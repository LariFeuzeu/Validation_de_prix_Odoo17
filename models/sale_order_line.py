from odoo import models, fields, api
from odoo.tools import float_compare


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    # Champ pour indiquer si le prix a été modifié par rapport au prix système
    need_price_validation = fields.Boolean(string="Prix changé", default=False,
                                           compute="_compute_need_price_validation",
                                           store=True)

    # Champ pour enregistrer le prix système (par exemple prix de référence interne)
    verified_price_unit = fields.Float(
        string="Prix Unité Verifié",
        compute='_compute_verified_price_unit',
        digits='Product Price',
        store=True)

    @api.depends('price_unit', 'verified_price_unit')
    def _compute_need_price_validation(self):
        # Cette méthode est appelée chaque fois que price_unit ou verified_price_unit est modifié
        for line in self:
            # Compare les deux prix avec une précision de 2 décimales
            # Si les prix sont différents alors need_price_validation = True
            line.need_price_validation = float_compare(
                line.price_unit,
                line.verified_price_unit,
                precision_digits=2
            ) != 0

    @api.depends('product_id', 'product_uom', 'product_uom_qty')
    def _compute_verified_price_unit(self):
        for line in self:
            # check if there is already invoiced amount. if so, the price shouldn't change as it might have been
            # manually edited
            if line.qty_invoiced > 0 or (line.product_id.expense_policy == 'cost' and line.is_expense):
                continue
            if not line.product_uom or not line.product_id:
                line.verified_price_unit = 0.0
            else:
                line = line.with_company(line.company_id)
                price = line._get_display_price()
                line.verified_price_unit = line.product_id._get_tax_included_unit_price_from_price(
                    price,
                    line.currency_id or line.order_id.currency_id,
                    product_taxes=line.product_id.taxes_id.filtered(
                        lambda tax: tax.company_id == line.env.company
                    ),
                    fiscal_position=line.order_id.fiscal_position_id,
                )