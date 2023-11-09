using Microsoft.AspNetCore.Mvc.Rendering;

namespace frontend.Interfaces
{
    public interface IDrpLstPuesto
    {
        public Task<List<SelectListItem>> GetDepartamentosForDropdown();
    }
}