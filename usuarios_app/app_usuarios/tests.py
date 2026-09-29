from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from .models import Usuario


class UsuariosFlowTests(TestCase):
	@patch("app_usuarios.services.usuarios_service.requests.get")
	def test_lista_carga_muestra_fija_y_abre_detalle(self, mock_get):
		mock_get.return_value.status_code = 200
		mock_get.return_value.json.return_value = {
			"results": [
				{
					"login": {"uuid": f"uuid-{index}"},
					"name": {"title": "Ms", "first": f"Nombre{index}", "last": "Prueba"},
					"email": f"usuario{index}@example.com",
					"gender": "female",
					"dob": {"age": 25},
					"location": {"city": "Quito"},
					"picture": {
						"large": "https://example.com/large.jpg",
						"medium": "https://example.com/medium.jpg",
						"thumbnail": "https://example.com/thumb.jpg",
					},
					"registered": {"date": "2020-01-01T00:00:00Z"},
				}
				for index in range(10)
			]
		}

		response = self.client.get(reverse("lista_usuarios"))

		self.assertEqual(response.status_code, 200)
		self.assertEqual(Usuario.objects.count(), 10)
		self.assertContains(response, "Nombre0 Prueba")
		mock_get.assert_called_once_with(
			"https://randomuser.me/api/",
			params={
				"page": 3,
				"results": 10,
				"seed": "eval-final-usuarios-2026-09-28",
			},
			timeout=10,
		)

		usuario = Usuario.objects.get(uuid="uuid-0")
		detalle = self.client.get(
			reverse("detalle_usuario", args=[usuario.uuid])
		)
		self.assertEqual(detalle.status_code, 200)
		self.assertContains(detalle, usuario.email)
		self.assertContains(detalle, usuario.imagen_large)
