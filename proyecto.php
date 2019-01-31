<?php
	//definicion de variables para la conexion a la DB proyecto
	$dbhost = "localhost"; //192.168.43.45 hotspot
	$dbuser = "jpcadena";
	$dbpass = "root1234";
	$dbname = "proyecto";
	$con = mysqli_connect($dbhost, $dbuser, $dbpass, $dbname);
	//validacion de la conexion con credenciales correctas
	if (!$con) {
    	echo "Error: Unable to connect to MySQL." . PHP_EOL;
    		echo "Debugging errno: " . mysqli_connect_errno() . PHP_EOL;
   		 echo "Debugging error: " . mysqli_connect_error() . PHP_EOL;
    		exit;
	}
	//metodo get para obtener valores 
	$Temperatura = $_GET['Temperatura'];
	$Humedad = $_GET['Humedad'];
        $UV = $_GET['UV'];
	//Insertando los valores en la tabla
	$query = "INSERT INTO valores(Temperatura, Humedad, UV) VALUES($Temperatura,$Humedad, $UV);";
	mysqli_real_query($con, $query);
	mysqli_close($con);
	// Imprimiendo los valores en la pagina
	echo "Datos sensados: <br />";
	echo "<br />Temperatura = $Temperatura ºC<br />";
	echo "<br />Humedad = $Humedad %<br />";
        echo "<br />Indice UV = $UV %<br />";
?>