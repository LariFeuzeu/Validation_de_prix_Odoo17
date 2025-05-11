from odoo import models, fields, api
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    need_price_validation = fields.Boolean(string="Changement de prix", default=False,
                                           compute="_compute_has_price_change", store=True)

    @api.depends('order_line.need_price_validation')
    def _compute_has_price_change(self):
        # Cette méthode vérifie s'il y a au moins une ligne avec un besoin de validation du prix
        for order in self:
            # Vérifie si une ligne a besoin d'une validation de prix
            order.need_price_validation = any(line.need_price_validation for line in order.order_line)

    def action_validate_price(self):
        # Cette méthode est appelée lorsque l'utilisateur valide les prix
        for order in self:
            # Réinitialise le besoin de validation de prix pour chaque ligne de commande
            for line in order.order_line:
                line.need_price_validation = False
            # Réinitialise le champ has_price_change pour la commande
            order.need_price_validation = False
        return True

    def action_confirm(self):

        for order in self:
            if order.need_price_validation:
                raise UserError("Veiller valider le prix avant de continuer")

            super(SaleOrder, self).action_confirm()
