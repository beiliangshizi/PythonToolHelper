#coding:utf-8
#author: beilianghsizi
#file: RedisWriter.py
#time: 2017/12/25 10:03
#desc: "Read taxi GPS point from csv file, then send to redis"

import redis, datetime, types
import codecs, kafka, time

TAXI_CSV = '/opt/RAW_DATA/TAXI_BACKUP/BK_2015-11-16/20151116.csv'
SRC_DATE = '2015-11-16'
SRC_UTC_FLAG = False
TAR_UTC_FLAG = True
DATETIME_FORMATTER = '%Y-%m-%d %X'

# VEHICLE_TYPE, VEHICLE_MODEL, VEHICLE_NUM,  PLATE_COLOR, RECORD_TIME ,        LONGITUDE,LATITUDE, STOWAGE, ALARM, OVER_SPEED_TIME, SPEED, DIRECTION, ALTITUDE, BUS_ROUTE, BUS_DIRECTION, RECEIVE_TIME
# 20,       A1,                苏A88322,     2,           2015-11-23 23:27:00, 118.69173,32.18058, 0,       0,     28800,           0.0,    0.0,      0.0,       ,         ,              2015-11-23 23:27:26, 2015-11-23 23:27:00,23:25:00,50616,320100,'
# 0         1                  2             3            4                    5         6         7        8      9                10      11        12         13        14             15
taxi_point = '20,A1,苏A88322,2,2015-11-23 23:27:00,118.69173,32.18058,0,0,28800,0.0,0.0,0.0,,,2015-11-23 23:27:26,2015-11-23 23:27:00,23:25:00,50616,320100,'


def localtoutc(t):
    st = datetime.datetime.strptime(t, DATETIME_FORMATTER) + datetime.timedelta(hours=-8)
    return st.strftime(DATETIME_FORMATTER)


class TaxiCSVParser(object):
    def __init__(self, name):
        self.name = name

    @staticmethod
    def __format(src):
        key, value = None, None
        try:
            # "DEVID", "LAT", "LNG", "SPEED", "GPS_TIME", "HEADING", "PASSENGER_STATE", "RECEIVE_TIME"
            s = src.split(',')
            gps_time, receive_time = localtoutc(s[4]), localtoutc(s[15])
            key = 'taxi_%s' % receive_time
            value = u'%s,%s,%s,%s,%s,%s,%s,%s' % (s[2], s[6], s[5], s[10], gps_time, s[11], s[7], receive_time)
        except Exception as e:
            print 'format failed:', src, e
        return key, value

    def gen(self):
        with codecs.open(TAXI_CSV, mode='r', encoding='utf8') as f:
            for line in f:
                yield self.__format(line)


class RedisIO(object):
    def __init__(self, host='localhost', port=6379):
        self.redis = redis.Redis(host=host, port=port, encoding='utf-8', charset='utf-8')
        self.pipeline = self.redis.pipeline()

    def add_to_list(self, list_name, value):
        if not isinstance(list_name, (str, unicode)) or not isinstance(value, (str, unicode)):
            print 'Invalid type', list_name, value
        else:
            self.pipeline.rpush(list_name, value)

    def commit(self):
        self.pipeline.execute()

    def get_list(self, name):
        if not isinstance(name, (str, unicode)):
            print 'Invalid type', name
            return None
        count = self.redis.llen(name)
        return self.redis.lrange(name, 0, count - 1)

    def clear_server_data(self):
        print '!!! Start to clear all server data'
        self.redis.flushall()
        print '!!! Clear done'

    def save(self):
        self.redis.save()


class KafkaIO(object):
    def __init__(self, broker, topic):
        self.broker = broker
        self.topic = topic
        self.__init_producer()

    def __init_producer(self):
        self.producer = kafka.KafkaProducer(bootstrap_servers=self.broker)

    def send(self, key, value):
        self.producer.send(self.topic, key=key, value=value)

    def flush(self):
        self.producer.flush()


def prepare_redis_data_from_csv(redis_client, csv):
    parser = TaxiCSVParser(csv)
    redis_client.clear_server_data()

    count = 0
    for k, v in parser.gen():
        redis_client.add_to_list(k, v)
        count = count + 1
        if count % 5000 == 0:
            print 'insert to redis:', count, k, v
            redis_client.commit()
            # redis_client.save()
        redis_client.commit()
    print 'insert to redis:', count


class TimeUtil(object):
    @staticmethod
    def now(utc=True):
        dt = datetime.datetime.now()
        if utc:
            dt = dt + datetime.timedelta(hours=-8)
        return dt

    @staticmethod
    def now_s(utc=True):
        dt = datetime.datetime.now()
        if utc:
            dt = dt + datetime.timedelta(hours=-8)
        return TimeUtil.to_string(dt)

    @staticmethod
    def localtoutc(dt):
        if isinstance(dt, datetime.datetime):
            return dt + datetime.timedelta(hours=8)
        return TimeUtil.localtoutc(TimeUtil.to_datetime(dt))

    @staticmethod
    def to_string(dt):
        return dt.strftime(DATETIME_FORMATTER)

    @staticmethod
    def to_datetime(dt):
        return datetime.datetime.strptime(dt, DATETIME_FORMATTER)

    @staticmethod
    def replace_date(str_dt, date):
        return ' '.join((date, str_dt[11:]))

    @staticmethod
    def get_time_list(ft, tt):
        if isinstance(ft, (str, unicode)):
            ft = TimeUtil.to_datetime(ft)
        if isinstance(tt, (str, unicode)):
            tt = TimeUtil.to_datetime(tt)
        delt = tt - ft
        tl = []
        seconds = (int)(delt.total_seconds())
        for i in xrange(seconds):
            tl.append(TimeUtil.to_string(ft + datetime.timedelta(seconds=i)))
        return tl


def format_record(record):
    record = unicode(record, 'utf-8')
    items = record.split(',')
    u = TimeUtil
    # "DEVID", "LAT", "LNG", "SPEED", "GPS_TIME", "HEADING", "PASSENGER_STATE", "RECEIVE_TIME"
    today = u.now_s()[:10]
    gps_time, receive_time = u.replace_date(items[4], today), u.replace_date(items[7], today)
    items[4], items[7] = gps_time, receive_time
    items[5] = unicode(int(float(items[5])))
    items.append("1")  # manual add plate color field
    return u','.join(items)


if __name__ == '__main__':
    redis = RedisIO(host='10.128.184.167')
    producer = KafkaIO(broker="10.128.184.167:9092", topic="topic_taxi")
    # prepare_redis_data_from_csv(redis, TAXI_CSV)

    t = TimeUtil
    from_time, to_time = t.now_s(), t.now_s()
    while 1:
        from_time, to_time = to_time, t.now_s()
        ft, tt = t.replace_date(from_time, SRC_DATE), t.replace_date(to_time, SRC_DATE)
        print "[%s, %s] => [%s, %s]" % (from_time, to_time, ft, tt)
        times = t.get_time_list(ft, tt)
        for dt in times:
            search_key = "taxi_%s" % dt
            key = t.replace_date(dt, t.now_s()[:10])
            records = redis.get_list(search_key)

            print "%s => %d [%s]" % (
                key, len(records), format_record(records[0]) if len(records) > 0 else '')
            for record in records:
                producer.send(key=key, value=format_record(record).encode('utf-8'))

        producer.flush()

        # redis.get_list("taxi_%s"%)
        time.sleep(3)