extends Node2D

const player_entity = preload("res://scenes/player_entity.tscn")

# Called when the node enters the scene tree for the first time.
func _ready():
	var player = player_entity.instantiate()
	var attributes = player.Player_Attributes.new()
	attributes.player_name = "Test"
	player.set_atributes(attributes)
	add_child(player)
	pass # Replace with function body.

func send_action():
	pass

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass
