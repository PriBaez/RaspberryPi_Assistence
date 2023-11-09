using System;
using Newtonsoft.Json;

namespace frontend.Models
{
    public class Empleado
    {
    public int Id { get; set; } 
    public string Nombre { get; set; } = null!;
    public string CorreoElectronico { get; set; }= null!;

    [JsonProperty("NumeroTelefono")]
    public string NumeroTelefono { get; set; } = null!;
    public DateTime FechaNacimiento { get; set; }
    public DateTime FechaIngreso { get; set; }
    public int IdPuestoEmpleado { get; set; }
    public bool Activo { get; set; }

    public Empleado()
    {}
    }

}