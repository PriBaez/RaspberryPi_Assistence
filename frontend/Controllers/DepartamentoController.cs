using frontend.Models;
using Microsoft.AspNetCore.Mvc;
using frontend.Interfaces;
using frontend.Services;
using System.Net;

namespace frontend.Controllers 
{
    
    public class DepartamentoController: Controller
    {
        private IDepartamentoService _service;
      
        public DepartamentoController(IDepartamentoService service)
        {
           _service = service;
        }
        public async Task<IActionResult> Listar()
        {
            var Departamentos = await _service.GetDepartamentos();
            return View(Departamentos);
        }
        
        public  IActionResult Guardar()
        {
            return View();
        }
        
        [HttpPost]
        public async Task<IActionResult> Guardar(Departamento departamento)
        {
            
            if(!ModelState.IsValid){
                return View();
            }
            try
            {
                
                HttpResponseMessage response = await _service.CrearDepartamento(departamento);
                
                if (response.StatusCode == HttpStatusCode.Created)
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
                                Console.WriteLine("Error en la solicitud POST, contacte al administrador. Código de estado: " + response.StatusCode);
                                return View();
                        }
            } catch (Exception ex) 
            {
                
                // Error en la solicitud
                Console.WriteLine("Error al realizar la solicitud POST, contacte al administrador:");
                Console.WriteLine(ex.Message);
            }
            
            return View();
        }

        public async Task<IActionResult> Editar(int id)
        {
            var DepartamentoToUpdate = await _service.GetDepartamentoById(id);
            return View(DepartamentoToUpdate);
        }

        [HttpPost]
        public async Task<IActionResult> Editar(int id, Departamento Departamento)
        {
            if(!ModelState.IsValid){
                Console.WriteLine("Modelo no valido.");
                return View();
            }

            Console.WriteLine("Voy al servicio a actualizar el departamento.");
            var respuesta = await _service.ActualizarDepartamento(id, Departamento);

            if(respuesta.IsSuccessStatusCode)
            {
                Console.WriteLine("Exito");
                return RedirectToAction("Listar");
            }
            else
                Console.WriteLine("Solicitud fallida.");
                return View();
        }

        public async Task<IActionResult> Eliminar(int Id)
        {
            var departamento = await _service.GetDepartamentoById(Id);
            return View(departamento);
        }

        [HttpPost]
        public async Task<IActionResult> Eliminar(int Id, Departamento departamento)
        {
           
            await Task.Delay(2000);
            Console.WriteLine($"tipo id: {Id.GetType()}");
            var respuesta = await _service.EliminarDepartamento(Id);

            if(respuesta.IsSuccessStatusCode)
                return RedirectToAction("Listar");
            else
                return View();
        }

    }

}