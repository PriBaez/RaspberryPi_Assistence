using frontend.Models;
using frontend.Services;

namespace frontend.Interfaces
{
    public interface IHistorialService
    {
        public Task<List<Historial>> GetHistorial();
        public Task<List<Historial>> GetHistorialperEmployee(int id);
       
    }
}