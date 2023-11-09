using Microsoft.AspNetCore.Mvc.Rendering;

namespace frontend.Interfaces
{
    public interface IDrpLstEmpleado
    {
        public Task<List<SelectListItem>> GetPuestosForDropdown();
    }
}