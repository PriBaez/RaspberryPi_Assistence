
namespace frontend.Models
{
    public class Historial
    {
         public int HistorialId { get; set; }
         public string PersonaId { get; set; } = null!;
         public DateTime FechaCaptura { get; set; }
    }
}