

function validarSenha(){
   senha = document.getElementById('senha_cliente').value;
   senha2 = document.getElementById('senha_confirmada_cliente').value;

   if(senha!= senha2) {
       alert("As senhas não conferem, verifique por favor !");
       return false;
   }
   return true;
}

$(document).ready(function($){

        $("#cpf_cliente").mask("000.000.000-00");
        $("#telefone_cliente").mask("(00)00000-0000");
        $("#CEP_endereco").mask("00000-000");
});
