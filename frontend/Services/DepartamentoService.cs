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
    public class DepartamentoService: IDepartamentoService
    {
        // IPAddressUtility utility = new IPAddressUtility();
        // private string ip_address = utility.GetIpAddress();
        private string ip_address = "http://172.16.32.224:5000";
        public async Task<List<Departamento>> GetDepartamentos()
        {
           
            using (HttpClient client = new HttpClient())
            {
                string apiUrl = $"{ip_address}/api/departamentos";

                try
                {
                    HttpResponseMessage response = await client.GetAsync(apiUrl);

                    if (response.IsSuccessStatusCode)
                    {
                        var content = await response.Content.ReadAsStringAsync();
                       
                        var deserializedData = string.IsNullOrEmpty(content) ? new List<Departamento>() : JsonConvert.DeserializeObject<List<Departamento>>(content);
                        return deserializedData != null ? deserializedData : new List<Departamento>();
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
            return new List<Departamento>();
        }

        public async Task<Departamento> GetDepartamentoById(int id)
        {
            // Implementar lógica para obtener un Departamento por su ID
            using (HttpClient client = new HttpClient())
            {
                string apiUrl = $"{ip_address}/api/departamento/{id}";

                try
                {
                    // Realizar una solicitud GET para obtener Departamentos
                    HttpResponseMessage response = await client.GetAsync(apiUrl);

                    if (response.IsSuccessStatusCode)
                    {
                        string content = await response.Content.ReadAsStringAsync();
                        var deserializedData = string.IsNullOrEmpty(content) ? new Departamento() : JsonConvert.DeserializeObject<Departamento>(content);
                        return deserializedData != null ? deserializedData : new Departamento();
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
            return new Departamento();
        }

        public async Task<HttpResponseMessage> CrearDepartamento(Departamento departamento)
        {
            string apiUrl = $"{ip_address}/api/departamento";

             using (HttpClient client = new HttpClient())
            {
                try
                {
                    string jsonData = JsonConvert.SerializeObject(departamento);
                    HttpResponseMessage response = await client.PostAsync(apiUrl, new StringContent(jsonData, System.Text.Encoding.UTF8, "application/json"));
                    return response;
                }
                catch (Exception ex){
                     Console.WriteLine($"Excepción: {ex.Message}");
                    return new HttpResponseMessage(HttpStatusCode.InternalServerError); 
                }
            }
        }

        public async Task<HttpResponseMessage> ActualizarDepartamento(int id, Departamento departamento)
        {
            string apiUrl = $"{ip_address}/api/departamento/{id}";

             using (HttpClient client = new HttpClient())
            {
                try
                {
                    string jsonData = JsonConvert.SerializeObject(departamento);
                    client.DefaultRequestHeaders.Add("Accept", "application/json");
                    HttpResponseMessage response = await client.PutAsync(apiUrl, new StringContent(jsonData, System.Text.Encoding.UTF8, "application/json"));
                    if (response.IsSuccessStatusCode)
                    {
                        Console.WriteLine("Departamento actualizado exitosamente.");
                    }
                    else
                    {
                        Console.WriteLine($"Error al actualizar el Departamento. Código de estado: {response.StatusCode}");
                    }
                    return response;

                } catch (Exception ex)
                {
                     Console.WriteLine($"Excepción: {ex.Message}");
                    return new HttpResponseMessage(HttpStatusCode.InternalServerError);
                }
            }
            
        }

        public async Task<HttpResponseMessage> EliminarDepartamento(int id)
        {
            string apiUrl = $"{ip_address}/api/departamento/{id}";

            using (HttpClient client = new HttpClient())
            {
                try
                {
                    HttpResponseMessage response = await client.DeleteAsync(apiUrl);

                    if (response.IsSuccessStatusCode)
                    {
                        Console.WriteLine("Departamento eliminado exitosamente.");
                    }
                    else
                    {
                        Console.WriteLine($"Error al eliminar el Departamento. Código de estado: {response.StatusCode}");
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
    
    }
}

