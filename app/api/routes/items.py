from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status

from app.api.dependencies import get_item_service
from app.api.schemas import (
    ErrorResponse,
    ItemCreate,
    ItemListResponse,
    ItemResponse,
    ItemUpdate,
)
from app.core.domain.item import Item
from app.core.services.item_service import ItemService

router = APIRouter(
    prefix="/items", tags=["items"], responses={404: {"model": ErrorResponse}}
)


@router.get(
    "/",
    response_model=ItemListResponse,
    summary="Get all items",
    description="Get a list of all items, with optional filtering by active status.",
)
async def get_items(
    service: Annotated[ItemService, Depends(get_item_service)],
    active: bool | None = Query(None, description="Filter by active status"),
) -> ItemListResponse:
    """Get all items, with optional filtering."""
    if active is not None:
        if active:
            items = await service.get_active_items()
        else:
            # Get all items and filter for inactive ones
            all_items = await service.get_all_items()
            items = [item for item in all_items if not item.is_active]
    else:
        items = await service.get_all_items()

    # Convert domain items to response format
    response_items = [ItemResponse.model_validate(item) for item in items]
    return ItemListResponse(items=response_items, count=len(items))


@router.get(
    "/{item_id}",
    response_model=ItemResponse,
    summary="Get item by ID",
    description="Get a specific item by its ID.",
    responses={404: {"model": ErrorResponse}},
)
async def get_item(
    service: Annotated[ItemService, Depends(get_item_service)],
    item_id: int = Path(..., description="The ID of the item to get"),
) -> ItemResponse:
    """Get a specific item by ID."""
    item = await service.get_item(item_id)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} not found",
        )
    return ItemResponse.model_validate(item)


@router.post(
    "/",
    response_model=ItemResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new item",
    description="Create a new item with the provided data.",
)
async def create_item(
    item_data: ItemCreate,
    service: Annotated[ItemService, Depends(get_item_service)],
) -> ItemResponse:
    """Create a new item."""
    # Convert API schema to domain model
    item = Item(
        name=item_data.name,
        description=item_data.description,
        price=item_data.price,
        is_active=item_data.is_active,
    )

    created_item = await service.create_item(item)
    return ItemResponse.model_validate(created_item)


@router.patch(
    "/{item_id}",
    response_model=ItemResponse,
    summary="Update an item",
    description="Update an existing item with the provided data.",
    responses={404: {"model": ErrorResponse}},
)
async def update_item(
    item_data: ItemUpdate,
    service: Annotated[ItemService, Depends(get_item_service)],
    item_id: int = Path(..., description="The ID of the item to update"),
) -> ItemResponse:
    """Update an existing item."""
    # First, get the existing item
    existing_item = await service.get_item(item_id)
    if existing_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} not found",
        )

    # Update only the fields that are provided
    update_data = item_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(existing_item, key, value)

    updated_item = await service.update_item(item_id, existing_item)
    return ItemResponse.model_validate(updated_item)


@router.delete(
    "/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an item",
    description="Delete an item by its ID.",
    responses={404: {"model": ErrorResponse}},
)
async def delete_item(
    service: Annotated[ItemService, Depends(get_item_service)],
    item_id: int = Path(..., description="The ID of the item to delete"),
) -> None:
    """Delete an item."""
    deleted = await service.delete_item(item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} not found",
        )
    return None


@router.get(
    "/search/",
    response_model=ItemListResponse,
    summary="Search items by name",
    description="Search for items by name (partial match).",
)
async def search_items(
    service: Annotated[ItemService, Depends(get_item_service)],
    name: str = Query(..., description="Name to search for"),
) -> ItemListResponse:
    """Search for items by name."""
    items = await service.search_items_by_name(name)
    response_items = [ItemResponse.model_validate(item) for item in items]
    return ItemListResponse(items=response_items, count=len(items))


@router.post(
    "/{item_id}/discount",
    response_model=ItemResponse,
    summary="Apply discount to an item",
    description="Apply a percentage discount to an item's price.",
    responses={404: {"model": ErrorResponse}},
)
async def apply_discount(
    service: Annotated[ItemService, Depends(get_item_service)],
    item_id: int = Path(..., description="The ID of the item"),
    discount_percent: float = Query(
        ..., gt=0, le=100, description="Discount percentage (0-100)"
    ),
) -> ItemResponse:
    """Apply a discount to an item."""
    updated_item = await service.apply_discount_to_item(item_id, discount_percent)
    if updated_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} not found",
        )
    return ItemResponse.model_validate(updated_item)
