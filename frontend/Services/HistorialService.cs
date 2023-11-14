using frontend.Interfaces;
using frontend.Models;
using Microsoft.AspNetCore.Mvc;
using Newtonsoft.Json;

namespace frontend.Services
{
    public class HistorialService: IHistorialService
    {
        static IPAddressUtility utility = new IPAddressUtility();

        public async Task<string> ip_address()
        {
            string hostname = await utility.GetIpAddress();
            await Task.Delay(2);
            return $"http://{hostname}:5000";
        } 
        public async Task<List<Historial>> GetHistorial()
        {
           
            using (HttpClient client = new HttpClient())
            {
                string hostname = await ip_address();
                await Task.Delay(2000);
                string apiUrl = $"{hostname}/api/historial";

                try
                {
                    HttpResponseMessage response = await client.GetAsync(apiUrl);

                    if (response.IsSuccessStatusCode)
                    {
                        var content = await response.Content.ReadAsStringAsync();
                       
                        var deserializedData = string.IsNullOrEmpty(content) ? new List<Historial>() : JsonConvert.DeserializeObject<List<Historial>>(content);
                        return deserializedData != null ? deserializedData : new List<Historial>();
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
            return new List<Historial>();
        }

        public async Task<List<Historial>> GetHistorialperEmployee(int id)
        {
            // Implementar lógica para obtener un Historial por su ID
            using (HttpClient client = new HttpClient())
            {
                string hostname = await ip_address();
                string apiUrl = $"{hostname}/api/historial/{id}";

                try
                {
                    // Realizar una solicitud GET para obtener Historial por persona
                    HttpResponseMessage response = await client.GetAsync(apiUrl);

                    if (response.IsSuccessStatusCode)
                    {
                        string content = await response.Content.ReadAsStringAsync();
                        var deserializedData = string.IsNullOrEmpty(content) ? new List<Historial>() : JsonConvert.DeserializeObject<List<Historial>>(content);
                        return deserializedData != null ? deserializedData : new List<Historial>();
                    }
                    else
                    {
                        Console.WriteLine($"La solicitud fue completada con errores : {response.StatusCode}\nDetalles: {response.RequestMessage}");
                    }
                }
                catch (Exception e)
                {
                    Console.WriteLine($"Error en la solicitud: {e.Message}");
                }
            }
            return new List<Historial>();
        }
    }
}
