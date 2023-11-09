using frontend.Services;
using frontend.Interfaces;
using Microsoft.AspNetCore.Mvc.Rendering;
using frontend.Models;
using frontend.Models.ViewData;
namespace frontend.Utils
{
     public class DrpLstEmpleado: IDrpLstEmpleado
    {
        private readonly IPuestoService _puestoService;
    
        public DrpLstEmpleado(IPuestoService puestoService)
        {
            _puestoService = puestoService;
        }

        public async Task<List<SelectListItem>> GetPuestosForDropdown()
        {
            var puestos =  await _puestoService.GetAllPuestos();

            List<ViewPuesto> lstPuesto = new List<ViewPuesto>();

            lstPuesto =(from p in puestos
                        select new ViewPuesto
                        {
                            IdPuestoEmpleado = p.IdPuestoEmpleado,
                            NombrePuesto = p.NombrePuesto,
                        }).ToList();

           
            List<SelectListItem> items = lstPuesto.ConvertAll(x => {
                return new SelectListItem()
                {
                    Text = x.NombrePuesto.ToString(),
                    Value = x.IdPuestoEmpleado.ToString(),
                    Selected = false
                };
            });

            return items;
        }    
    }
}