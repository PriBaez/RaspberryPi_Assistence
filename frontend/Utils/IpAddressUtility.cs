using System;
using System.Net;
using System.Threading.Tasks;

public class IPAddressUtility
{
    public async Task<string> GetIpAddress()
    {
        // Obtiene el nombre del host de la Raspberry Pi
        string hostName = "raspberryPB";

        try
        {
            // Obtiene la dirección IP asociada con el nombre del host
            IPAddress[] addresses = await Dns.GetHostAddressesAsync(hostName);
            //await Task.Delay(2000);

            foreach (IPAddress address in addresses)
            {
                // Filtra las direcciones IPv4
                if (address.AddressFamily == System.Net.Sockets.AddressFamily.InterNetwork)
                {
                    Console.WriteLine(address);
                    return address.ToString();
                }
            }

            Console.WriteLine("No se encontraron direcciones IPv4.");
            return "Error";
        }
        catch (Exception e)
        {
            Console.WriteLine($"Error al obtener la dirección IP: {e.Message}");
            return "Error";
        }
    }
}
