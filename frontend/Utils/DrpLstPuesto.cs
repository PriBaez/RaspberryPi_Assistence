using frontend.Services;
using frontend.Interfaces;
using Microsoft.AspNetCore.Mvc.Rendering;
using frontend.Models;
using frontend.Models.ViewData;
namespace frontend.Utils
{
     public class DrpLstPuesto: IDrpLstPuesto
    {
        private readonly IDepartamentoService _departamentoService;
    
        public DrpLstPuesto(IDepartamentoService departamentoService)
        {
            _departamentoService = departamentoService;
        }

        public async Task<List<SelectListItem>> GetDepartamentosForDropdown()
        {
            var departamentos =  await _departamentoService.GetDepartamentos();

            List<Departamento> lstDepartamentos = new List<Departamento>();

            lstDepartamentos =(from p in departamentos
                        select new Departamento
                        {
                            IdDepartamento = p.IdDepartamento,
                            NombreDepartamento = p.NombreDepartamento,
                        }).ToList();

            Console.WriteLine(lstDepartamentos.ToString());
            
            List<SelectListItem> items = lstDepartamentos.ConvertAll(x => {
                return new SelectListItem()
                {
                    Text = x.NombreDepartamento,
                    Value = x.IdDepartamento.ToString(),
                    Selected = false
                };
            });

            return items;
        }    
    }
}