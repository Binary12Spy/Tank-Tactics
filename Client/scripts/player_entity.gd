extends Node2D

const DEFAULT_PLAYER_NAME = "Player"

# Player attributes
var player_id:String
var player_name:String
var health:int
var action_points:int
var range:int
var location:Array
var is_player:bool

# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.

func set_atributes(attributes):
	player_name = attributes.player_name || DEFAULT_PLAYER_NAME
	health = attributes.health
	is_player = attributes.is_player
	action_points = attributes.action_points
	range = attributes.range
	location = attributes.location
	update_location()
	pass

func update_location():
	pass

func on_hover():
	print(self.player_name)
	pass

func off_hover():
	print(self.health)
	pass

func on_rclick(viewport, event, shape_idx):
	pass

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass
