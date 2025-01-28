import abc
from typing import Set
from allocation.adapters import orm
from allocation.domain import model


class AbstractRepository(abc.ABC):
    def __init__(self):
        self.seen = set()  # type: Set[model.Product]

    def add(self, product: model.Product):
        self._add(product)
        self.seen.add(product)

    def get(self, sku) -> model.Product:
        product = self._get(sku)
        if product:
            self.seen.add(product)
        return product

    def get_by_batchref(self, batchref) -> model.Product:
        product = self._get_by_batchref(batchref)
        if product:
            self.seen.add(product)
        return product

    def _add(self, product: model.Product):
        """
        Add a product to the repository.

        This method is part of the Unit of Work pattern, as it ensures
        that the product is added to the repository as part of the unit
        of work's commit process. This helps maintain consistency and
        ensures that the product is only added if the unit of work is
        successfully committed.
        """
        raise NotImplementedError

    def _get(self, sku) -> model.Product:
        """
        Get a product from the repository by SKU.

        This method is part of the Unit of Work pattern, as it ensures
        that the product is retrieved from the repository as part of the
        unit of work's commit process. This helps maintain consistency
        and ensures that the product is only retrieved if the unit of
        work is successfully committed.
        """
        raise NotImplementedError

    def _get_by_batchref(self, batchref) -> model.Product:
        """
        Get a product from the repository by batch reference.

        This method is part of the Unit of Work pattern, as it ensures
        that the product is retrieved from the repository as part of the
        unit of work's commit process. This helps maintain consistency
        and ensures that the product is only retrieved if the unit of
        work is successfully committed.
        """
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        super().__init__()
        self.session = session

    def _add(self, product):
        self.session.add(product)

    def _get(self, sku):
        return self.session.query(model.Product).filter_by(sku=sku).first()

    def _get_by_batchref(self, batchref):
        return (
            self.session.query(model.Product)
            .join(model.Batch)
            .filter(
                orm.batches.c.reference == batchref,
            )
            .first()
        )
