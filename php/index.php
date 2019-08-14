<?php

function h($s) { return htmlentities($s); }
function u($s) { return rawurlescape($s); }
function hu($s) { return h(u($s)); }
function tt($s) { return '<tt>'.h($s).'</tt>'; }

$ID = 'currentlyplays';
$DIR = '/tmp/';
$SRC = "$DIR$ID.in";
$DST = "$DIR$ID.out";

$src = NULL;
$user = "unknown";
?>
<!DOCTYPE html>
<html>
<head>
<meta http-equiv="content-type" content="text/html;charset=UTF-8">
<title>Currently playing</title>
<style>
</style>
</head>
<body class="full">
<?php try { ?>
<?php

  $src	= @json_decode(file_get_contents($SRC));
?>
<?php if (!is_object($src)): ?>
<div>
Cannot parse <?=tt($SRC)?> - is the background service running?
</div>
<?php elseif ($src['ask']): ?>
<form method="POST" action="?<?=hu($src['arg'])?>">
<label for="input"><?=h($src['ask'])?></label>
<input type="text" width="60" id="input" name="value"/>
</form>
<?php
    else:
?>
T.B.D.
<?php endif ?>
<?php } catch (Exception $e) { ?>
<div>
Internal error: <?=h($e)?>
</div>
<?php } ?>
</body>
</html>
