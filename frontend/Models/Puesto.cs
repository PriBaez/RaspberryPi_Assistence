using System;

namespace frontend.Models
{
    public class Puesto
    {
        public int IdPuestoEmpleado { get; set; }
        public string NombrePuesto { get; set; } = null!;
        public string Descripcion { get; set; } = null!;
        public int IdDepartamento { get; set; }
    }
}