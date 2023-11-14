using frontend.Models;
using Microsoft.AspNetCore.Mvc;
using frontend.Interfaces;
using frontend.Services;

namespace frontend.Controllers 
{
    
    public class PuestoController: Controller
    {
        private IPuestoService _service;
        private IDrpLstPuesto _drpLst;
    
        public PuestoController(IPuestoService service, IDrpLstPuesto drpLst)
        {
           _service = service;
           _drpLst = drpLst;
        }
        public async Task<IActionResult> Listar()
        {
            var puestos = await _service.GetAllPuestos();
            var departamentos = await _drpLst.GetDepartamentosForDropdown();
            await Task.Delay(2000);
            ViewBag.Departamentos = departamentos;
            return View(puestos);
        }
        
        public  async Task<IActionResult> Guardar()
        {
           
            var departamentos = await _drpLst.GetDepartamentosForDropdown();
            ViewBag.Departamentos = departamentos;
            await Task.Delay(2000);
            return View();
        }
        
        [HttpPost]
        public async Task<IActionResult> Guardar(Puesto puesto)
        {
            
            if(!ModelState.IsValid){
                return View();
            }
            try
            {
               
                HttpResponseMessage response = await _service.CreatePuesto(puesto);
                await Task.Delay(2000);
                var content = "";
                if (response.IsSuccessStatusCode)
                        {
                            // La solicitud fue exitosa
                            content = await response.Content.ReadAsStringAsync();
                            // Aquí puedes procesar la respuesta como desees
                            ViewBag.SuccessMessage = "Solicitud POST exitosa. Respuesta del servidor: " + content;
                                return RedirectToAction("Listar");
                        }
                        else
                        {
                            ViewBag.ErrorMessage = "Error: la solicitud fue completada con errores, contacte al administrador. Código de estado: " + response.StatusCode;
                            return View();
                        }
            } catch (Exception ex) 
            {
                
                // Error en la solicitud
                ViewBag.ErrorMessage = "Error al realizar la solicitud POST, contacte al administrador: " + ex.Message;
                Console.WriteLine("Error en la solicitud:", ex.Message);
            }
            
            return View();
        }

        public async Task<IActionResult> Editar(int id)
        {
            var puestoToUpdate = await _service.GetPuestoById(id);
            await Task.Delay(2000); 
            var departamentos = await _drpLst.GetDepartamentosForDropdown();
            ViewBag.Departamentos = departamentos;
            return View(puestoToUpdate);
        }

        [HttpPost]
          public async Task<IActionResult> Editar(int id, Puesto puesto)
        {
            if(!ModelState.IsValid){
                return View();
            }

            var respuesta = await _service.UpdatePuesto(id, puesto);

            if(respuesta.IsSuccessStatusCode)
                return RedirectToAction("Listar");
            else
                return View();
        }
        public async Task<IActionResult> Eliminar(int id)
        {
            var puesto = await _service.GetPuestoById(id);
            Console.WriteLine(puesto.IdPuestoEmpleado);
            return View(puesto);
        }

        [HttpPost]
        public async Task<IActionResult> Eliminar(Puesto puesto)
        {
            var respuesta = await _service.DeletePuesto(puesto.IdPuestoEmpleado);

             if(respuesta.IsSuccessStatusCode)
                return RedirectToAction("Listar");
            else
                return View();
        }

    }

}