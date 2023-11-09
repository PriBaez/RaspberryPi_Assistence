using System;
using System.Collections.Generic;
using System.Net;
using System.Reflection.Metadata.Ecma335;
using System.Text.RegularExpressions;
using frontend.Interfaces;
using frontend.Models;
using Microsoft.AspNetCore.Mvc;
using Newtonsoft.Json;

namespace frontend.Services
{
    public class EmpleadoService: IEmpleadoService
    {
        // IPAddressUtility utility = new IPAddressUtility();
        // private string ip_address = utility.GetIpAddress();
        private string ip_address = "http://172.16.32.224:5000";
        public async Task<List<Empleado>> GetEmpleados()
        {
           
            using (HttpClient client = new HttpClient())
            {
                string apiUrl = $"{ip_address}/api/empleados";

                try
                {
                    HttpResponseMessage response = await client.GetAsync(apiUrl);

                    if (response.IsSuccessStatusCode)
                    {
                        var content = await response.Content.ReadAsStringAsync();

                        content = AdjustDateFormats(content);
                       
                        var deserializedData = string.IsNullOrEmpty(content) ? new List<Empleado>() : JsonConvert.DeserializeObject<List<Empleado>>(content);
                        return deserializedData != null ? deserializedData : new List<Empleado>();
                    }
                    else
                    {
                        Console.WriteLine($"Error en la solicitud: {response.StatusCode}\nDetalles: {response.RequestMessage}");
                    }
                }
                catch (Exception e)
                {
                    Console.WriteLine($"Error en la solicitud: {e.Message}");
                }
            }
            return new List<Empleado>();
        }

        public async Task<Empleado> GetEmpleadoById(int id)
        {
            // Implementar lógica para obtener un empleado por su ID
            using (HttpClient client = new HttpClient())
            {
                string apiUrl = $"{ip_address}/api/empleado/{id}";

                try
                {
                    // Realizar una solicitud GET para obtener empleados
                    HttpResponseMessage response = await client.GetAsync(apiUrl);

                    if (response.IsSuccessStatusCode)
                    {
                        string content = await response.Content.ReadAsStringAsync();
                        content = AdjustDateFormats(content);
                        var deserializedData = string.IsNullOrEmpty(content) ? new Empleado() : JsonConvert.DeserializeObject<Empleado>(content);
                        return deserializedData != null ? deserializedData : new Empleado();
                    }
                    else
                    {
                        Console.WriteLine($"Error en la solicitud: {response.StatusCode}\nDetalles: {response.RequestMessage}");
                    }
                }
                catch (Exception e)
                {
                    Console.WriteLine($"Error en la solicitud: {e.Message}");
                }
            }
            return new Empleado();
        }

        public async Task<HttpResponseMessage> CrearEmpleado(Empleado empleado)
        {
            string apiUrl = $"{ip_address}/api/empleado";

             using (HttpClient client = new HttpClient())
            {
                try
                {
                    empleado.Activo = true;  
                    string jsonData = JsonConvert.SerializeObject(empleado);
                    client.DefaultRequestHeaders.Add("Accept", "application/json");
                    HttpResponseMessage response = await client.PostAsync(apiUrl, new StringContent(jsonData, System.Text.Encoding.UTF8, "application/json"));
                    return response;
                }
                catch {
                    Console.WriteLine("Ecepcion");
                    return new HttpResponseMessage(HttpStatusCode.InternalServerError); 
                }
            }
        }

        public async Task<HttpResponseMessage> ActualizarEmpleado(int id, Empleado empleado)
        {
            string apiUrl = $"{ip_address}/api/empleado/{id}";

             using (HttpClient client = new HttpClient())
            {
                try
                {
                    string jsonData = JsonConvert.SerializeObject(empleado);
                    client.DefaultRequestHeaders.Add("Accept", "application/json");
                    HttpResponseMessage response = await client.PutAsync(apiUrl, new StringContent(jsonData, System.Text.Encoding.UTF8, "application/json"));
                    if (response.IsSuccessStatusCode)
                    {
                        Console.WriteLine("Empleado actualizado exitosamente.");
                    }
                    else
                    {
                        Console.WriteLine($"Error al actualizar el empleado. Código de estado: {response.StatusCode}");
                    }
                    return response;

                } catch 
                {
                    Console.WriteLine("Ecepcion");
                    return new HttpResponseMessage(HttpStatusCode.InternalServerError);
                }
            }
            
        }

        public async Task<HttpResponseMessage> EliminarEmpleado(int id)
        {
            string apiUrl = $"{ip_address}/api/empleado/{id}";

            using (HttpClient client = new HttpClient())
            {
                try
                {
                    HttpResponseMessage response = await client.DeleteAsync(apiUrl);

                    if (response.IsSuccessStatusCode)
                    {
                        Console.WriteLine("Empleado eliminado exitosamente.");
                    }
                    else
                    {
                        Console.WriteLine($"Error al eliminar el empleado. Código de estado: {response.StatusCode}");
                    }

                    return response;
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"Excepción: {ex.Message}");
                    return new HttpResponseMessage(HttpStatusCode.InternalServerError); 
                }
            }
                    
        }
    

       private string AdjustDateFormats(string content)
       {  
        
        content = content.Replace("T00", " 00");
        return content;
       }
    }
}

