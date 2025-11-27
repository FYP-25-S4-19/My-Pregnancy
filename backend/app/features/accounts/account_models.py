from app.core.custom_base_model import CustomBaseModel

# class DoctorAccountCreationRequest(CustomBaseModel):
#     username: str
#     email: EmailStr
#     password: str
#     full_name: str
#     role: UserRole


# class NutritionistAccountCreationRequest(CustomBaseModel):
#     username: str
#     email: EmailStr
#     password: str
#     full_name: str
#     role: UserRole


class AccountCreationRequestView(CustomBaseModel):
    first_name: str
    middle_name: str | None = None
    last_name: str
    qualification_option: str
    qualification_img_url: str
