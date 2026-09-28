from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List


@dataclass
class Role:
    id: Optional[int] = None
    name: str = ""
    slug: str = ""
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class Permission:
    id: Optional[int] = None
    name: str = ""
    slug: str = ""
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class UserRole:
    id: Optional[int] = None
    user_id: Optional[str] = None
    role_id: Optional[int] = None
    role_slug: Optional[str] = None
    created_at: Optional[datetime] = None


@dataclass
class RoleHasPermission:
    id: Optional[int] = None
    role_id: Optional[int] = None
    permission_id: Optional[int] = None
    created_at: Optional[datetime] = None
