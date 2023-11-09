using System.Collections.Generic;
using System.Threading.Tasks;
using frontend.Models;

namespace frontend.Interfaces
{
    public interface IPuestoService
    {
        Task<List<Puesto>> GetAllPuestos();
        Task<Puesto> GetPuestoById(int id);
        Task<HttpResponseMessage> CreatePuesto(Puesto puesto);
        Task<HttpResponseMessage> UpdatePuesto(int id, Puesto puesto);
        Task<HttpResponseMessage> DeletePuesto(int id);
    }
}
