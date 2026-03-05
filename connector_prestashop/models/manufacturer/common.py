# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

from odoo.addons.component.core import Component

from ...components.backend_adapter import PrestaShopWebServiceImage

_logger = logging.getLogger(__name__)


class ProductBrand(models.Model):
    _inherit = "product.brand"

    prestashop_bind_ids = fields.One2many(
        comodel_name="prestashop.manufacturer",
        inverse_name="odoo_id",
        string="PrestaShop Bindings",
    )


class PrestashopManufacturer(models.Model):
    _name = "prestashop.manufacturer"
    _inherit = "prestashop.binding.odoo"
    _inherits = {"product.brand": "odoo_id"}
    _description = "Manufacturer prestashop bindings"

    odoo_id = fields.Many2one(
        comodel_name="product.brand",
        string="Product Brand",
        required=True,
        ondelete="cascade",
    )
    date_add = fields.Datetime(
        string="Created At (on PrestaShop)",
        readonly=True,
    )
    date_upd = fields.Datetime(
        string="Updated At (on PrestaShop)",
        readonly=True,
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        required=True,
        default=lambda self: self.env.company.id,
    )


class ManufacturerAdapter(Component):
    _name = "prestashop.manufacturer.adapter"
    _inherit = "prestashop.adapter"
    _apply_on = "prestashop.manufacturer"
    _prestashop_model = "manufacturers"
    _export_node_name = "manufacturer"
    _export_node_name_res = "manufacturer"
