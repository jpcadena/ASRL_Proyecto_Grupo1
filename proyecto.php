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
	//seleccion de los ultimos datos en la tabla
	$query2="select * from valores order by id desc limit 1";
	$result = mysqli_query($con, $query2);

	//tabla  en HTML
	echo "<html>";
	echo "<body>";
	echo "<br>";
	echo "<table style='border-collapse: collapse;' align='center'>";
	echo "<legend style='text-align:center'>Tabla de Resultados</legend>";
	echo "<tr>";
    	echo "<td style='padding:5px 10px;font-size: 16px;background-color: #83aec0;border-right-width: 3px;border-left-width: 3px;border-bottom-width: 1px;border-right-style: solid;border-left-style: solid;border-bottom-style: solid;border-right-color: #558FA6;border-left-color: #558FA6;border-bottom-color: #558FA6;text-align:center;color:white';font-weight:bold;>Fecha</td>";
    	echo "<td style='padding:5px 10px;font-size: 16px;background-color: #83aec0;border-right-width: 3px;border-bottom-width: 1px;border-right-style: solid;border-bottom-style: solid;border-right-color: #558FA6;border-bottom-color: #558FA6;text-align:center;color:white;font-weight:bold;'>Temperatura</td>";
    	echo "<td style='padding:5px 10px;font-size: 16px;background-color: #83aec0;border-right-width: 3px;border-bottom-width: 1px;border-right-style: solid;border-bottom-style: solid;border-right-color: #558FA6;border-bottom-color: #558FA6;text-align:center;color:white;font-weight:bold;'>Humedad</td>";
    	echo "<td style='padding:5px 10px;font-size: 16px;background-color: #83aec0;border-right-width: 3px;border-bottom-width: 1px;border-right-style: solid;border-bottom-style: solid;border-right-color: #558FA6;border-bottom-color: #558FA6;text-align:center;color:white;font-weight:bold;'>Indice UV</td>";
    	echo "</tr>";
	while ($row = mysqli_fetch_assoc($result)) { // Important line !!! Check summary get row on array ..
    		echo "<tr>";
    		foreach ($row as $field => $value) { // I you want you can right this line like this: foreach($row as $value) {
        		echo "<td style='padding:5px 10px;color: #34484E;background-color: #e2ebef;border-right-width: 1px;border-bottom-width: 1px;border-right-style: solid;border-bottom-style: solid;border-left-width: 1px;border-left-style: solid;border-left-color: #A4C4D0;border-right-color: #A4C4D0;border-bottom-color: #A4C4D0;text-align:center'>" . $value . "</td>"; // I just did not use "htmlspecialchars()" function. 
    		}
    		echo "</tr>";
	}
	echo "</table>";

	mysqli_real_query($con, $query);
	mysqli_close($con);

	// Imprimiendo los valores en la pagina
	echo "Datos sensados: <br />";
	echo "<br />Temperatura = $Temperatura ºC<br />";
	echo "<br />Humedad = $Humedad %<br />";
        echo "<br />Indice UV = $UV %<br />";
	echo "</body>";
	echo "</html>";
?>
