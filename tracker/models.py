# file: models/task_models.py
from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional, List, Dict, Any

from sqlalchemy import (
    String, Integer, BigInteger, ForeignKey, Text, Boolean, Float,
    DateTime, JSON, UniqueConstraint, Index
)
from sqlalchemy.orm import (
    DeclarativeBase, Mapped, mapped_column, relationship
)

class Base(DeclarativeBase):
    pass


def utcnow() -> datetime:
    return datetime.now(timezone.utc)   

class Task(Base):
    __tablename__ = "task"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    # 기본 정보
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # 담당/요청
    assigned_to: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    requester: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)

    # 분류/상태
    task_type: Mapped[str] = mapped_column(String(50), default="general")   # sw, human, doc ...
    status: Mapped[str] = mapped_column(String(30), default="draft")        # draft, in_progress, blocked, done ...
    priority: Mapped[int] = mapped_column(Integer, default=3)               # 1~5

    # 일정
    due: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # parent/subtask 구조
    parent_id: Mapped[Optional[int]] = mapped_column(
        BigInteger, ForeignKey("task.id", ondelete="SET NULL"), nullable=True
    )

    # audit
    created_by: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    updated_by: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, onupdate=utcnow)

    # task_meta (checklist 포함)
    metas: Mapped[List["TaskMeta"]] = relationship(
        "TaskMeta",
        back_populates="task",
        cascade="all, delete-orphan",
        order_by="TaskMeta.sort_order.asc(), TaskMeta.id.asc()"
    )

    # task dependency
    dependencies: Mapped[List["TaskDependency"]] = relationship(
        "TaskDependency",
        foreign_keys="TaskDependency.task_id",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    __table_args__ = (
        Index("ix_task_assigned_to", "assigned_to"),
        Index("ix_task_requester", "requester"),
        Index("ix_task_status", "status"),
        Index("ix_task_due", "due"),
        Index("ix_task_parent_id", "parent_id"),
    )


 #이건 task_meta로 옮기자
 # 예상치 (task-level)
    est_hours: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    est_cost: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    est_difficulty: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # 1~10
    
    # 캐시 (목록 화면 빠르게)
    progress: Mapped[float] = mapped_column(Float, default=0.0)       # 0~100
    blocking_count: Mapped[int] = mapped_column(Integer, default=0)

    # 기타
    extra: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)

class TaskDependency(Base):
    """
    오직 task 간 dependency만 표현:
    task_id 가 depends_on_task_id 를 기다림
    """
    __tablename__ = "task_dependency"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    task_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("task.id", ondelete="CASCADE"), nullable=False
    )
    depends_on: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("task.id", ondelete="CASCADE"), nullable=False
    )

    # critical dependency 여부만 남김 (단순)
    is_critical: Mapped[bool] = mapped_column(Boolean, default=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)

    __table_args__ = (
        UniqueConstraint("task_id", "depends_on_task_id", name="uq_task_dependency"),
        Index("ix_task_dependency_task_id", "task_id"),
        Index("ix_task_dependency_depends_on_task_id", "depends_on_task_id"),
    )


class TaskMeta(Base):
    __tablename__ = "task_meta"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    task_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("task.id", ondelete="CASCADE"), nullable=False
    )

    # meta 종류: check_item, note, record_link, signal ...
    meta_type: Mapped[str] = mapped_column(String(40), nullable=False, default="check_item")

    # 표시용
    title: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)


        # check_item 계산용 (meta_type='check_item'일 때 사용)
    done: Mapped[bool] = mapped_column(Boolean, default=False)
    is_required: Mapped[bool] = mapped_column(Boolean, default=True)
    is_blocking: Mapped[bool] = mapped_column(Boolean, default=False)

    # 느슨한 순서 (10,20,30...)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

    # 계획/난이도 (가중치 계산용)
    planned_hours: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    planned_cost: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    difficulty: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # 1~10
    weight: Mapped[Optional[float]] = mapped_column(Float, nullable=True)       # 직접 지정 가능

    # records 연결용 (선택)
    source_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)  # email, github, note...
    source_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
