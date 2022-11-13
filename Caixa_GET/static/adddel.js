$(document).ready(function(){    
     
      var subtotal = 0;
      var i=1;
      var n = document.getElementById('tabel_preco').className;
      $("#add_row").click(function(event){
        event.preventDefault();
        var select = document.getElementById('codigo');
        var value = select.selectedIndex + 1//select.options[select.selectedIndex].value;
        var lista_produtos = [];



        //console.log("N linhas = "+n)
        //console.log("value "+value)
        //console.log( document.getElementById(j).className );
        for(j=1;j<=n;j++){
          if(j == value){
            //console.log(j == value);
            var select1 = document.getElementById(j).className;  //nome do produto
            //console.log("slect "+select1+" j "+j);
          }
        
        }

      for(k=1;k<=n;k++){
        if(k+"a" == value+"a"){
          var select2 = document.getElementById(k+"a").className;  //preço
        }
        
      }

      for(x=1;x<=n;x++){
        if(x+"b" == value+"b"){
          var select3 = document.getElementById(x+"b").className;  //sku
        }
        
      }
      
      b=i-1;

      //elementos tr e td
      var tr = document.createElement("tr");
      tr.className = "tr"+i;
      var td = document.createElement("td");
      td.className = "td_nome"+i;
      td.name = "sku";
      var tdb = document.createElement("td");
      tdb.className = "td_local"+i;
      tdb.id = select2;
      tdb.name = "preco"
      var tdc = document.createElement("td");
      tdc.className = "td_rec"+i;
      tdc.name = "produto";

      //elementos input
      //var quantidade = document.createElement('input'); //crio um elemento do tipo input

      /*var local = document.createElement('label'); //crio um elemento do tipo input
      var recipiente = document.createElement('label'); //crio um elemento do tipo input
      var nome = document.createElement("label");*/
      var local = document.createElement('input'); //crio um elemento do tipo input
      var recipiente = document.createElement('input'); //crio um elemento do tipo input
      var nome = document.createElement("input");



      local.className = "form-control text-center justify-content-center";
      local.name = "preco";
      local.value = select2;
      local.readOnly = true;
      recipiente.className = "form-control text-center justify-content-center";
      recipiente.name = "produto";
      recipiente.value = select1;
      recipiente.readOnly = true;
      nome.className = "form-control text-center justify-content-center";
      nome.name = "sku";
      nome.value = select3;
      nome.readOnly = true;
      

      //anexando ao table
      document.querySelector('#tabela').appendChild(tr);

      document.querySelector(".tr"+i).appendChild(td);
      document.querySelector(".tr"+i).appendChild(tdc);
      //document.querySelector(".tr"+i).appendChild(tda);
      document.querySelector(".tr"+i).appendChild(tdb);
      //document.querySelector("#addr0").className + CHR(65+i);
      document.querySelector(".td_nome"+i).appendChild(nome);
      document.querySelector(".td_local"+i).appendChild(local);
      document.querySelector(".td_rec"+i).appendChild(recipiente);
     /* document.querySelector(".td_nome"+i).innerHTML = select3;//document.querySelector("#addr0").className + String.fromCharCode(65+i)//CHR(65+i); sku
      document.querySelector(".td_rec"+i).innerHTML = select1;//appendChild(recipiente); produto
      document.querySelector(".td_local"+i).innerHTML = select2;//appendChild(local); preco*/

      
      

      subtotal += parseFloat(select2);
      //console.log(subtotal)
      //console.log(document.querySelector(".td_local"+i).className)
      i++; 
      document.querySelector(".subtotal").innerHTML = "Subtotal: R$ " + subtotal.toFixed(2);
  });
     
    $("#delete_row").click(function(event){
      event.preventDefault();
      if(i>1){
        //console.log(document.querySelector(".td_local"+(i-1)).id);
        subtotal -= parseFloat(document.querySelector(".td_local"+(i-1)).id);
        //console.log(document.querySelector(".td_local"+(i-1)));
        $(".tr"+(i-1)).html('');
        i--;
        document.querySelector(".subtotal").innerHTML = "Subtotal: R$ " + subtotal.toFixed(2);
      }
    });


    $("#fim_pagamento").click(function(event){
       event.preventDefault();
       if(i>0){
          cupom = document.querySelector(".cod_cliente").value;
          //console.log(cupom)    
          if(cupom>20000){
            document.querySelector(".subtotal").innerHTML = "Subtotal: R$ " + (0.8*subtotal).toFixed(2);
            troco = parseFloat(document.querySelector(".pagamento").value) - 0.8*subtotal;
            document.querySelector(".troco").innerHTML = "Troco: R$ " + troco.toFixed(2);
          }else if(cupom>=0){
            document.querySelector(".subtotal").innerHTML = "Subtotal: R$ " + (0.8*subtotal).toFixed(2);
            troco = parseFloat(document.querySelector(".pagamento").value) - 0.8*subtotal;
            document.querySelector(".troco").innerHTML = "Troco: R$ " + troco.toFixed(2);
          }
          else{
            troco = parseFloat(document.querySelector(".pagamento").value) - subtotal;
            document.querySelector(".troco").innerHTML = "Troco: R$ " + troco.toFixed(2);
          }   
       }
      
    });




});


