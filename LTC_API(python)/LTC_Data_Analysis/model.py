from index import db


class alarm_history_data(db.Document):
	collcetion_latest_id= db.StringField()
	base_topic    = db.StringField()
	dst          = db.StringField()
	src          = db.StringField()
	seq	         = db.StringField()
	SNR	         = db.StringField()
	RSSIpkt      = db.StringField()
	BW           = db.StringField()
	CR           = db.StringField()
	SF           = db.StringField()
	sensor_id    = db.StringField()
	version      = db.StringField()
	command_id   = db.StringField()
	data_length  = db.StringField()
	data         = db.StringField()
	mote_lat     = db.StringField()
	mote_lon     = db.StringField()
	time         = db.StringField()
	distance2base= db.StringField()