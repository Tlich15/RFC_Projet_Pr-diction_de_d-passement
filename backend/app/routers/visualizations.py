from io import BytesIO

import matplotlib
from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import Response

from ..services import data_loader

# Use non-interactive backend
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402

router = APIRouter()


@router.get("/client-history.png", response_class=Response)
def plot_client_history(client: str = Query(..., description="Client name")) -> Response:
    history = data_loader.get_client_history(client)
    if not history:
        raise HTTPException(status_code=404, detail="No history for client")

    # Prepare data
    dates = [row.get("Date_Mois") for row in history]
    values = [row.get("Depassement") or row.get("Décompte") or 0 for row in history]

    # Plot
    fig, ax = plt.subplots(figsize=(8, 3))
    ax.plot(dates, values, marker='o', linewidth=1.5)
    ax.set_title(f"Historique - {client}")
    ax.set_xlabel("Mois")
    ax.set_ylabel("Valeur")
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    buf = BytesIO()
    fig.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return Response(content=buf.getvalue(), media_type="image/png")