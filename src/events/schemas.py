from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, date


class Event(BaseModel):
    platformv: str = ""
    event_name: str
    profile_age: int = 0
    user_agent: str = ""
    screen: str = ""
    event_datetime_str: str = ""
    event_datetime: datetime
    event_date: date
    auth_method: str = ""
    auth_type: str = ""
    request_id: str = ""
    referer: str = ""
    subscription_name: str = ""
    subscription_id: str = ""
    deeplink: str = ""
    payment_type: str = ""
    transaction_id: str = ""
    purchase_option: str = ""
    content_type: str = ""
    content_gid: str = ""
    content_name: str = ""
    content_id: str = ""
    promocode: str = ""
    promocode_code: str = ""
    quality: str = ""
    play_url: str = ""
    channel_name: str = ""
    channel_id: str = ""
    channel_gid: str = ""
    cause: str = ""
    button_id: str = ""
    button_text: str = ""
    feedback_text: str = ""
    experiments: str = ""
    season: str = ""
    episode: str = ""
    discount_items_ids: str = ""
    discount_items_names: str = ""
    content_provider: str = ""
    story_type: str = ""
    userId: str = ""
    playtime_ms: Optional[int]
    duration: Optional[int]
    client_id: str
    discount: str = ""
    is_trial: Optional[int]
    price: int = 0
    dt_add: datetime
    url_user_event: str = ""
    event_receive_timestamp: int = 0
    event_receive_dt_str: str = ""
    shelf_name: str = ""
    shelf_index: Optional[int]
    card_index: Optional[int]
    error_message: str = ""
    platform_useragent: str = ""
    product_id: str
    dl: str = ""
    fp: str = ""
    dr: str = ""
    mc: int = 0
    r: str
    sc: int = 0
    sid: str
    sr: str = ""
    title: str = ""
    ts: Optional[datetime]
    wr: str = ""
    cid: str = ""
    uid: str = ""
    ll: str = ""
    av: str = ""
    os: str = ""
    mnf: str = ""
    mdl: str = ""
    os_family: str = ""
    os_version: str = ""
    is_mobile: int = 0
    is_pc: int = 0
    is_tablet: int = 0
    is_touch_capable: int = 0
    client_id_body: str = ""
    client_id_query: str
    time: int = 0
    field_id: str = ""
    field_action: str = ""
    search_films: str = ""
    recommended_films: str = ""
    event_datetime_msc: Optional[datetime]
    user_device_is_tv: int = 0
    input_type: str = ""
    product_names: str = ""
    product_ids: str = ""
    prices: str = ""
    auth_status_list: str = ""
    isJunior: str = ""
    waterbase_device_id: str
    error_url: str = ""
    error_severity: int = 999
    error_category: int = 999
    error_code: str = ""
    os_build: str = ""
    banner_type: str = ""
    banner_id: str = ""
    banner_gid: str = ""
    kion_session_id: str = ""
    popup_name: str = ""
    popup_action: str = ""
    app_version: str = ""
    downloaded: int = 999
    osv: str = ""
    dt: str = ""
    dm: str = ""
    lc: str = ""
    event_source: str = ""
    device_id: str = ""
    debug: bool = False
    host: str = ""
    path: str = ""
    request_type: str = ""
    code: str = ""
    message: str = ""
    field_text: str = ""
    card_gid: str = ""
    current_time: Optional[int]
    card_id: str = ""
    card_type: str = ""
    card_name: str = ""
    uuid: str = ""
    term: str = ""
    playing_mode: str = ""
    inserted_dt: Optional[datetime]
    build_model: str = ""
    build_manufacturer: str = ""
    extra_field: str = ""
    trouble_report: str = ""
    playback_speed: str = ""
