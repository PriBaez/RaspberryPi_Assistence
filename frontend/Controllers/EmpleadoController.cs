using frontend.Models;
using Microsoft.AspNetCore.Mvc;
using frontend.Interfaces;
using frontend.Services;

namespace frontend.Controllers 
{
    
    public class EmpleadoController: Controller
    {
        private IEmpleadoService _service;
        private IDrpLstEmpleado _drpLst;
        public EmpleadoController(IEmpleadoService service, IDrpLstEmpleado drpLst)
        {
           _service = service;
           _drpLst = drpLst;
        }
        public async Task<IActionResult> Listar()
        {
            var empleados = await _service.GetEmpleados();
            var puestos = await _drpLst.GetPuestosForDropdown();
            ViewBag.Puestos = puestos;
            return View(empleados);
        }
        
        public async  Task<IActionResult> Guardar()
        {
            try
            {

                var puestos = await _drpLst.GetPuestosForDropdown();
                ViewBag.Puestos = puestos;
                return View();
                
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex);
            }

            return View();
            
        }
        
        [HttpPost]
        public async Task<IActionResult> Guardar(Empleado empleado)
        {
            Console.WriteLine($"Id:{empleado.Id}\nNombre:{empleado.Nombre}\nIdPuestoEmpleado:{empleado.IdPuestoEmpleado}");
            if(!ModelState.IsValid){
                return View();
            }

            try
            {
                
                HttpResponseMessage response = await _service.CrearEmpleado(empleado);
                
                if (response.StatusCode == System.Net.HttpStatusCode.Created )
                        {
                            // La solicitud fue exitosa
                            var content = await response.Content.ReadAsStringAsync();
                            // Aquí puedes procesar la respuesta como desees
                            ViewBag.SuccessMessage = "Solicitud POST exitosa. Respuesta del servidor: " + content;
                                return RedirectToAction("Listar");
                        }
                        else
                        {
                            // La solicitud no fue exitosa, manejar el error
                            ViewBag.ErrorMessage = "Error en la solicitud POST, contacte al administrador. Código de estado: " + response.StatusCode;
                                return View();
                        }
            } catch (Exception ex) 
            {
                
                // Error en la solicitud
                ViewBag.ErrorMessage = "Error al realizar la solicitud POST, contacte al administrador: " + ex.Message;
                Console.WriteLine(ex.Message);
            }
            
            return View();
        }

        public async Task<IActionResult> Editar(int Id)
        {
            var empleado = await _service.GetEmpleadoById(Id);
            var puestos = await _drpLst.GetPuestosForDropdown();
            ViewBag.Puestos = puestos;
            return View(empleado);
        }

        [HttpPost]
        public async Task<IActionResult> Editar(Empleado empleado)
        {
            if(!ModelState.IsValid){
                return View();
            }

            var respuesta = await _service.ActualizarEmpleado(empleado.Id, empleado);

            if(respuesta.IsSuccessStatusCode)
                return RedirectToAction("Listar");
            else
                return View();
        }

        public async Task<IActionResult> Eliminar(int Id)
        {
            var empleado = await _service.GetEmpleadoById(Id);
            return View(empleado);
        }

        [HttpPost]
        public async Task<IActionResult> Eliminar(Empleado empleado)
        {
            var respuesta = await _service.EliminarEmpleado(empleado.Id);

            if(respuesta.IsSuccessStatusCode)
                return RedirectToAction("Listar");
            else
                return View();
        }

    }

}