from pysolar.solar import get_altitude, get_azimuth
from datetime import datetime
from pytz import timezone


def getSolarPosition(
    latitude: float = -0.2105367,
    longitude: float = -78.491614,
    date: datetime = datetime.now(tz=timezone("America/Guayaquil")),
):
    """
    Calcula azimuth y elevation del Sol para una posición geográfica.

    Returns
    -------
    azimuth : float
        Ángulo en grados [0, 360)
    elevation : float
        Elevación solar en grados [-90, 90]
    """
    az = get_azimuth(latitude, longitude, date)
    el = get_altitude(latitude, longitude, date)
    return az, el
