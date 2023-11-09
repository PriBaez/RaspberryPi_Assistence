using System;
using System.Net;

public class IPAddressUtility
{
    public string GetIpAddress()
    {
        try
        {
            // Obtiene el nombre del host de la Raspberry Pi
            string hostName = "raspberryPB";
            // Obtiene la dirección IP asociada con el nombre del host
            IPAddress[] addresses = Dns.GetHostAddresses(hostName);

            foreach (IPAddress address in addresses)
            {
                // Filtra las direcciones IPv4
                if (address.AddressFamily == System.Net.Sockets.AddressFamily.InterNetwork)
                {
                    return address.ToString();
                }
            }
        }
        catch (Exception e)
        {
            return e.Message;
        }

        return "No se pudo obtener la dirección IP. Verifica la conectividad de red.";
    }
}