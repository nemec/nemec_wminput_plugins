import wmplugin
import cwiid
import math

acc_zero = None
acc_one = None
acc = [0,0,0]

NEW_AMOUNT = 0.1
OLD_AMOUNT = 1 - NEW_AMOUNT

Roll_Scale = 1
Pitch_Scale = 1
X_Scale = 1
Y_Scale = 1

def wmplugin_info():
  return ["brake", "acc_left", "acc_right", "accel", "left", "right"], [], []

def wmplugin_init(id, wiimote):
  global acc_zero, acc_one

  wmplugin.set_rpt_mode(id, cwiid.RPT_ACC)
  acc_zero, acc_one = wiimote.get_acc_cal(cwiid.EXT_NONE)
  return

def wmplugin_exec(mesg):

  global acc_zero, acc_one, acc

  buttons = [False, False, False, False, False, False]

  for m in mesg:
    if m[0] == cwiid.MESG_ACC:
      acc = [NEW_AMOUNT*(new-zero)/(one-zero) + OLD_AMOUNT*old
             for old,new,zero,one in zip(acc,m[1],acc_zero,acc_one)]
      a = math.sqrt(sum(map(lambda x: x**2, acc)))

      roll = math.atan(acc[cwiid.X]/acc[cwiid.Z])
      if acc[cwiid.Z] <= 0:
        if acc[cwiid.X] > 0: roll += math.pi
        else: roll -= math.pi

      pitch = math.atan(acc[cwiid.Y]/acc[cwiid.Z]*math.cos(roll))

      if roll < -2.0:
        buttons[0] = True
        print "brake"
      elif roll > -0.7:
        if pitch > 0.8:
          buttons[1] = True
          print "acc_left"
        elif pitch < -0.8:
          buttons[2] = True
          print "acc_right"
        else:
          buttons[3] = True
          print "accel"
      elif pitch > 0.8:
        buttons[4] = True
        print "left"
      elif pitch < -0.8:
        buttons[5] = True
        print "right"

  return buttons, []

