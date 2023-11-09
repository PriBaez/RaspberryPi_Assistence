using frontend.Models;
using frontend.Services;

namespace frontend.Interfaces
{
    public interface IEmpleadoService
    {
        public Task<List<Empleado>> GetEmpleados();
        public Task<Empleado> GetEmpleadoById(int id);
        public Task<HttpResponseMessage> CrearEmpleado(Empleado empleado);
        public Task<HttpResponseMessage> ActualizarEmpleado(int id, Empleado empleado);
        public Task<HttpResponseMessage> EliminarEmpleado(int id);
    }
}