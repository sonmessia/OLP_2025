"""
Predefined areas for traffic monitoring
"""
from typing import Dict, List, Tuple, Optional
from pydantic import BaseModel


class AreaBounds(BaseModel):
    """Area bounds model"""
    name: str
    bounds: List[List[float]]  # [[south, west], [north, east]]
    center: List[float]  # [lat, lon]
    tls_id: str


# Predefined areas
AREAS: Dict[str, AreaBounds] = {
    "nga_tu_thu_duc": AreaBounds(
        name="Ngã Tư Thủ Đức",
        bounds=[[10.848, 106.77], [10.855, 106.778]],
        center=[10.8515, 106.774],
        tls_id="4066470692"
    ),
    "hang_xanh": AreaBounds(
        name="Ngã Tư Hàng Xanh",
        bounds=[[10.798, 106.698], [10.805, 106.706]],
        center=[10.8015, 106.702],
        tls_id="hang_xanh_tls"
    )
}


def get_area_by_tls_id(tls_id: str) -> Optional[AreaBounds]:
    """Get area by traffic light ID"""
    for area in AREAS.values():
        if area.tls_id == tls_id:
            return area
    return None


def get_area_by_name(name: str) -> Optional[AreaBounds]:
    """Get area by name"""
    return AREAS.get(name)
