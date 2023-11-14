using frontend.Models;
using Microsoft.AspNetCore.Mvc;
using frontend.Interfaces;
using frontend.Services;

namespace frontend.Controllers 
{
    
    public class HistorialController: Controller
    {
        private IHistorialService _service;
        public HistorialController(IHistorialService service)
        {
           _service = service;
        }
        public async Task<IActionResult> Listar()
        {
            var Historial = await _service.GetHistorial();
            return View(Historial);
        }

        public async Task<IActionResult> ListarPorEmpleado(int id)
        {
            var Historial = await _service.GetHistorialperEmployee(id);
            return View(Historial);
        }
    }    
}