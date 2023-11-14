using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using frontend.Models;
using frontend.Interfaces;
using Newtonsoft.Json;
using System.Net;
using System.Net.Http.Headers;

namespace frontend.Services
{
    public class PuestoService : IPuestoService
    {
    
       static IPAddressUtility utility = new IPAddressUtility();

        public async Task<string> ip_address()
        {
            string hostname = await utility.GetIpAddress();
            await Task.Delay(2);
            return $"http://{hostname}:5000";
        } 
        public async Task<List<Puesto>> GetAllPuestos()
        {
            using (HttpClient client = new HttpClient())
            {
                string hostname = await ip_address();
                string apiUrl = $"{hostname}/api/puesto";

                try
                {
                    client.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));
                    HttpResponseMessage response = await client.GetAsync(apiUrl);

                    if (response.IsSuccessStatusCode)
                    {
                        // Leer y mostrar la respuesta JSON
                        var content = await response.Content.ReadAsStringAsync();
                        var deserializedData = string.IsNullOrEmpty(content) ? new List<Puesto>() : JsonConvert.DeserializeObject<List<Puesto>>(content);
                        return deserializedData != null ? deserializedData : new List<Puesto>();
                    }
                    else
                    {
                        Console.WriteLine($"Error en la solicitud GET de puestos: {response.StatusCode}\nDetalles: {response.RequestMessage}");
                    }
                }
                catch (Exception e)
                {
                    Console.WriteLine($"Error en la solicitud GET de puestos: {e.Message}");
                }
            }
            return new List<Puesto>();
        }

        public async Task<Puesto> GetPuestoById(int id)
        {
            using (HttpClient client = new HttpClient())
            {
                string hostname = await ip_address();

                string apiUrl = $"{hostname}/api/puesto/{id}";

                try
                {
                    client.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));
                    HttpResponseMessage response = await client.GetAsync(apiUrl);

                    if (response.IsSuccessStatusCode)
                    {
                        // Leer y mostrar la respuesta JSON
                        string content = await response.Content.ReadAsStringAsync();
                        var deserializedData = string.IsNullOrEmpty(content) ? new Puesto() : JsonConvert.DeserializeObject<Puesto>(content);
                        return deserializedData != null ? deserializedData : new Puesto();
                    }
                    else
                    {
                        Console.WriteLine($"Error en la solicitud: {response.StatusCode}\nDetalles: {response.RequestMessage}");
                    }
                }
                catch (Exception e)
                {
                    Console.WriteLine($"Error en la solicitud GET puesto: {e.Message}");
                    Console.WriteLine(apiUrl);
                }
            }
            return new Puesto();
        }

        public async Task<HttpResponseMessage> CreatePuesto(Puesto puesto)
        {
            string hostname = await ip_address();
            string apiUrl = $"{hostname}/api/puesto";

             using (HttpClient client = new HttpClient())
            {
                try
                {
                    string jsonData = JsonConvert.SerializeObject(puesto);
                    HttpResponseMessage response = await client.PostAsync(apiUrl, new StringContent(jsonData, System.Text.Encoding.UTF8, "application/json"));
                    return response;
                }
                catch (Exception e) {
                    Console.WriteLine("Excepcion: " + e.Message);
                    return new HttpResponseMessage(HttpStatusCode.InternalServerError);
                }
            }
        }

        public async Task<HttpResponseMessage> UpdatePuesto(int id, Puesto puesto)
        {
           string hostname = await ip_address();
           string apiUrl = $"{hostname}/api/puesto/{id}";

             using (HttpClient client = new HttpClient())
            {
                try
                {

                    string jsonData = JsonConvert.SerializeObject(puesto);
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

        public async Task<HttpResponseMessage> DeletePuesto(int id)
        {
            string hostname = await ip_address();
            string apiUrl = $"{hostname}/api/puesto/{id}";

            using (HttpClient client = new HttpClient())
            {
                try
                {
                    HttpResponseMessage response = await client.DeleteAsync(apiUrl);

                    if (response.IsSuccessStatusCode)
                    {
                        Console.WriteLine("Puesto eliminado exitosamente.");
                    }
                    else
                    {
                        Console.WriteLine($"Error al eliminar el puesto. Código de estado: {response.StatusCode}");
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
