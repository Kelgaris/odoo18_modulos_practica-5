odoo -u lista_tareas -d odoo-db --stop-after-init
xit
docker restart odoo
exit
odoo -u lista_tareas -d odoo-db --stop-after-init
exit
cd /mnt/extra-addons/
./odoo-bin -d odoo -u EJ09-LigaFutbol --stop-after-init
exit
