
const registroUsu = document.getElementById('RegistroUsu');
const inputs = document.querySelectorAll('#RegistroUsu input, select')


const expresiones = {
	Nombre: /^[a-zA-ZÀ-ÿ\s]{1,40}$/, // Letras y espacios, pueden llevar acentos.
	apellido: /^[a-zA-ZÀ-ÿ\s]{1,40}$/, // Letras y espacios, pueden llevar acentos.
	password: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+])[a-zA-Z0-9!@#$%^&*()_+]{4,20}$/,
	correo: /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]{2,}$/, // Correo electrónico válido con cualquier dominio
	telefono: /^\d{10}$/, // 10 números exactamente.
	documento: /^\d{8,10}$/, // Entre 8 y 10 números.
	select: /^(?!Seleccione).*$/, // El valor del select no debe empezar con "Seleccione"
	fecha: /^\d{4}-\d{2}-\d{2}$/, // Fecha en formato "YYYY-MM-DD"

}

const campos = {
	Nombre: false,
	apellido: false,
	correo: false,
	telefono: false,
	documento: false,
	select: false,
	fecha: false
}
const validarFormulario = (e) => {
	switch (e.target.name) {
		case "nombre_persona":
			validadorCampo(expresiones.Nombre, e.target, 'nombre');
			break;

		case "apellido_persona":
			validadorCampo(expresiones.apellido, e.target, 'apellido');
			break;

		case "num_documento":
			validadorCampo(expresiones.documento, e.target, 'documento');
			break;

		case "Telefono":
			validadorCampo(expresiones.telefono, e.target, 'telefono');
			break;

		case "CorreoE":
			validadorCampo(expresiones.correo, e.target, 'email');
			break;

		case "Fecha_de_nacimiento":
			validadorCampo(expresiones.fecha, e.target, 'fecha');
			break;

		case "tiDocumento":
			validadorCampo(expresiones.select, e.target, 'select');
			break;

		case "genero":
			validadorCampo(expresiones.select, e.target, 'genero');
			break;


	}
}

const validadorCampo = (expresion, input, campo) => {
	if (campo === 'select' || campo === 'genero') {
		if (input.value !== '') {
			document.getElementById(`grupo__${campo}`).classList.remove('col-incorrecto');
			document.getElementById(`grupo__${campo}`).classList.add('col-correcto');
			document.querySelector(`#grupo__${campo} i`).classList.add('fa-check-circle');
			document.querySelector(`#grupo__${campo} i`).classList.remove('fa-circle-xmark');
			document.querySelector(`#grupo__${campo} .formulario__input-Error`).classList.remove('formulario__input-Error-activo');
			campos[campo] = true;
		} else {
			document.getElementById(`grupo__${campo}`).classList.add('col-incorrecto');
			document.getElementById(`grupo__${campo}`).classList.remove('col-correcto');
			document.querySelector(`#grupo__${campo} i`).classList.add('fa-circle-xmark');
			document.querySelector(`#grupo__${campo} i`).classList.remove('fa-check-circle');
			document.querySelector(`#grupo__${campo} .formulario__input-Error`).classList.add('formulario__input-Error-activo');
			campos[campo] = false;
		}
	} else {
		if (expresion.test(input.value)) {
			document.getElementById(`grupo__${campo}`).classList.remove('col-incorrecto');
			document.getElementById(`grupo__${campo}`).classList.add('col-correcto');
			document.querySelector(`#grupo__${campo} i`).classList.add('fa-check-circle');
			document.querySelector(`#grupo__${campo} i`).classList.remove('fa-circle-xmark');
			document.querySelector(`#grupo__${campo} .formulario__input-Error`).classList.remove('formulario__input-Error-activo');
			campos[campo] = true;
		} else {
			document.getElementById(`grupo__${campo}`).classList.add('col-incorrecto');
			document.getElementById(`grupo__${campo}`).classList.remove('col-correcto');
			document.querySelector(`#grupo__${campo} i`).classList.add('fa-circle-xmark');
			document.querySelector(`#grupo__${campo} i`).classList.remove('fa-check-circle');
			document.querySelector(`#grupo__${campo} .formulario__input-Error`).classList.add('formulario__input-Error-activo');
			campos[campo] = false;
		}
	}
};

const validarpassword = () => {
	const inputContra = document.getElementById('password');
	const inputContra2 = document.getElementById('confirm_password');

	if (inputContra.value !== inputContra2.value) {
		document.getElementById(`grupo__password`).classList.add('col-incorrecto');
		document.getElementById(`grupo__password`).classList.remove('col-correcto');
		document.querySelector(`#grupo__password i`).classList.add('fa-circle-xmark');
		document.querySelector(`#grupo__password i`).classList.remove('fa-check-circle');
		document.querySelector(`#grupo__password .formulario__input-Error`).classList.add('formulario__input-Error-activo');
		campos['password'] = false;
	} else {
		document.getElementById(`grupo__password`).classList.remove('col-incorrecto');
		document.getElementById(`grupo__password`).classList.add('col-correcto');
		document.querySelector(`#grupo__password i`).classList.remove('fa-circle-xmark');
		document.querySelector(`#grupo__password i`).classList.add('fa-check-circle');
		document.querySelector(`#grupo__password .formulario__input-Error`).classList.remove('formulario__input-Error-activo');
		campos['confirm_password'] = false;
	}
};


inputs.forEach((input) => {
	input.addEventListener('keyup', validarFormulario);
	input.addEventListener('blur', validarFormulario);
});



document.getElementById('RegistroUsu').addEventListener('submit', function(event) {
	event.preventDefault(); // Evita el envío del formulario por defecto

	Swal.fire({
	  icon: 'question',
	  title: 'Confirmar datos',
	  text: '¿Estás seguro de que deseas enviar el formulario?',
	  showCancelButton: true,
	  confirmButtonText: 'Sí',
	  cancelButtonText: 'No'
	}).then((result) => {
	  if (result.isConfirmed) {
		// Si se confirma la acción, se envía el formulario
		event.target.submit();
	  } else if (result.dismiss === Swal.DismissReason.cancel) {
		// Si se cancela la acción, no se envía el formulario
		Swal.fire('Cancelado', 'El envío del formulario ha sido cancelado.', 'info');
	  }
	});
  });   


