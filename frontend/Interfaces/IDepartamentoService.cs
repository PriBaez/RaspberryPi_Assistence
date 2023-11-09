using frontend.Models;
using frontend.Services;

namespace frontend.Interfaces
{
    public interface IDepartamentoService
    {
        public Task<List<Departamento>> GetDepartamentos();
        public Task<Departamento> GetDepartamentoById(int id);
        public Task<HttpResponseMessage> CrearDepartamento(Departamento Departamento);
        public Task<HttpResponseMessage> ActualizarDepartamento(int id, Departamento Departamento);
        public Task<HttpResponseMessage> EliminarDepartamento(int id);
    }
}