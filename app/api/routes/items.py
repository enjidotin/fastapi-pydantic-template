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
    prefix="/items",
    tags=["items"],
    responses={404: {"model": ErrorResponse}}
)


@router.get(
    "/", 
    response_model=ItemListResponse,
    summary="Get all items",
    description="Get a list of all items, with optional filtering by active status."
)
async def get_items(
    active: bool | None = Query(None, description="Filter by active status"),
    service: ItemService = Depends(get_item_service),
):
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
    
    return ItemListResponse(items=items, count=len(items))


@router.get(
    "/{item_id}", 
    response_model=ItemResponse,
    summary="Get item by ID",
    description="Get a specific item by its ID.",
    responses={404: {"model": ErrorResponse}}
)
async def get_item(
    item_id: int = Path(..., description="The ID of the item to get"),
    service: ItemService = Depends(get_item_service),
):
    """Get a specific item by ID."""
    item = await service.get_item(item_id)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} not found"
        )
    return item


@router.post(
    "/", 
    response_model=ItemResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new item",
    description="Create a new item with the provided data."
)
async def create_item(
    item_data: ItemCreate,
    service: ItemService = Depends(get_item_service),
):
    """Create a new item."""
    # Convert API schema to domain model
    item = Item(
        name=item_data.name,
        description=item_data.description,
        price=item_data.price,
        is_active=item_data.is_active
    )
    
    created_item = await service.create_item(item)
    return created_item


@router.patch(
    "/{item_id}", 
    response_model=ItemResponse,
    summary="Update an item",
    description="Update an existing item with the provided data.",
    responses={404: {"model": ErrorResponse}}
)
async def update_item(
    item_data: ItemUpdate,
    item_id: int = Path(..., description="The ID of the item to update"),
    service: ItemService = Depends(get_item_service),
):
    """Update an existing item."""
    # First, get the existing item
    existing_item = await service.get_item(item_id)
    if existing_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} not found"
        )
    
    # Update only the fields that are provided
    update_data = item_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(existing_item, key, value)
    
    updated_item = await service.update_item(item_id, existing_item)
    return updated_item


@router.delete(
    "/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an item",
    description="Delete an item by its ID.",
    responses={404: {"model": ErrorResponse}}
)
async def delete_item(
    item_id: int = Path(..., description="The ID of the item to delete"),
    service: ItemService = Depends(get_item_service),
):
    """Delete an item."""
    deleted = await service.delete_item(item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} not found"
        )
    return None


@router.get(
    "/search/", 
    response_model=ItemListResponse,
    summary="Search items by name",
    description="Search for items by name (partial match)."
)
async def search_items(
    name: str = Query(..., description="Name to search for"),
    service: ItemService = Depends(get_item_service),
):
    """Search for items by name."""
    items = await service.search_items_by_name(name)
    return ItemListResponse(items=items, count=len(items))


@router.post(
    "/{item_id}/discount",
    response_model=ItemResponse,
    summary="Apply discount to an item",
    description="Apply a percentage discount to an item's price.",
    responses={404: {"model": ErrorResponse}}
)
async def apply_discount(
    item_id: int = Path(..., description="The ID of the item"),
    discount_percent: float = Query(..., 
                                   gt=0, 
                                   le=100, 
                                   description="Discount percentage (0-100)"),
    service: ItemService = Depends(get_item_service),
):
    """Apply a discount to an item."""
    updated_item = await service.apply_discount_to_item(item_id, discount_percent)
    if updated_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} not found"
        )
    return updated_item 