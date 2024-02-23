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
                Console.WriteLine($"Dirección IP encontrada: {address}");
                // Filtra las direcciones IPv4
                if (address.AddressFamily == System.Net.Sockets.AddressFamily.InterNetwork)
                {
                    Console.WriteLine(address);
                    return address.ToString();
                }
            }

            string ipv6Addr = GetIPv6Address(hostName);
            return ipv6Addr;
        }
        catch (Exception e)
        {
            Console.WriteLine($"Error al obtener la dirección IP: {e.Message}");
            return "Error";
        }
    }

    public static string GetIPv6Address(string hostname)
    {
        try
        {
            IPHostEntry ipEntry = System.Net.Dns.GetHostEntry(hostname);
            IPAddress[] addresses = ipEntry.AddressList;

             // Busca la última dirección IPv6 en la lista
                foreach (var address in addresses)
                {
                    if (address.AddressFamily == System.Net.Sockets.AddressFamily.InterNetworkV6)
                    {
                        return address.ToString();
                    }
                }
            
            return "No Ipv6 address found";
        }
        catch (Exception)
        {
            Console.WriteLine("Error occurred while retrieving the IP address.");
            return "Error";
        }
    }
}
