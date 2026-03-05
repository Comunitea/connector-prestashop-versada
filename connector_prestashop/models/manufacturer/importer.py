# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import datetime
import logging

from odoo.addons.component.core import Component
from odoo.addons.connector.components.mapper import mapping

_logger = logging.getLogger(__name__)


class ManufacturerMapper(Component):
    _name = "prestashop.manufacturer.mapper"
    _inherit = "prestashop.import.mapper"
    _apply_on = "prestashop.manufacturer"

    direct = [
        ("name", "name"),
        ("description", "description"),
    ]

    @mapping
    def backend_id(self, record):
        return {"backend_id": self.backend_record.id}

    @mapping
    def company_id(self, record):
        return {"company_id": self.backend_record.company_id.id}

    @mapping
    def date_add(self, record):
        if record.get("date_add") in ("0000-00-00 00:00:00", False, None):
            return {"date_add": datetime.datetime.now()}
        return {"date_add": record["date_add"]}

    @mapping
    def date_upd(self, record):
        if record.get("date_upd") in ("0000-00-00 00:00:00", False, None):
            return {"date_upd": datetime.datetime.now()}
        return {"date_upd": record["date_upd"]}

    @mapping
    def description(self, record):
        description = None
        if "language" in record["description"]:
            language_binder = self.binder_for("prestashop.res.lang")
            languages = record["description"]["language"]
            if not isinstance(languages, list):
                languages = [languages]
            for lang in languages:
                erp_language = language_binder.to_internal(lang["attrs"]["id"])
                if not erp_language:
                    continue
                if erp_language.code == "en_US":
                    description = lang["value"]
                    break
            if description is None:
                description = languages[0]["value"]
        else:
            description = record["description"]
        return {"description": description}


class ManufacturerImporter(Component):
    """Import one manufacturer record from PrestaShop as a product.brand"""

    _name = "prestashop.manufacturer.importer"
    _inherit = "prestashop.importer"
    _apply_on = "prestashop.manufacturer"

    def _create(self, record):
        return super()._create(record)


class ManufacturerBatchImporter(Component):
    _name = "prestashop.manufacturer.batch.importer"
    _inherit = "prestashop.delayed.batch.importer"
    _apply_on = "prestashop.manufacturer"
