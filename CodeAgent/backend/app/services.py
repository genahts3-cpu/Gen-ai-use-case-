import uuid
from typing import List
from .models import UseCase, UseCaseCreate, UseCaseUpdate
from .storage import load_usecases, save_usecases


def list_usecases() -> List[UseCase]:
    return load_usecases()


def create_usecase(payload: UseCaseCreate) -> UseCase:
    usecases = load_usecases()
    new_usecase = UseCase(
        id=str(uuid.uuid4()),
        title=payload.title,
        description=payload.description,
        industry=payload.industry,
        business_value=payload.business_value,
        tags=payload.tags or [],
        status=payload.status or "draft",
    )
    usecases.append(new_usecase)
    save_usecases(usecases)
    return new_usecase


def update_usecase(usecase_id: str, payload: UseCaseUpdate) -> UseCase:
    usecases = load_usecases()
    for idx, uc in enumerate(usecases):
        if uc.id == usecase_id:
            updated = uc.model_copy(update=payload.model_dump(exclude_unset=True))
            usecases[idx] = updated
            save_usecases(usecases)
            return updated
    raise KeyError("Use case not found")


def delete_usecase(usecase_id: str) -> None:
    usecases = load_usecases()
    filtered = [uc for uc in usecases if uc.id != usecase_id]
    if len(filtered) == len(usecases):
        raise KeyError("Use case not found")
    save_usecases(filtered)


def search_usecases(query: str) -> List[UseCase]:
    query_lower = query.lower()
    results = []
    for uc in load_usecases():
        if (
            query_lower in uc.title.lower()
            or query_lower in uc.description.lower()
            or query_lower in uc.industry.lower()
            or query_lower in uc.business_value.lower()
            or any(query_lower in t.lower() for t in uc.tags)
        ):
            results.append(uc)
    return results
