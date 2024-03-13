import os

import win32com.client


def add_to_taskschd():
    print('Adding to taskschd...')
    TASK_TRIGGER_LOGON = 9
    TASK_CREATE_OR_UPDATE = 6
    TASK_ACTION_EXEC = 0
    TASK_LOGON_INTERACTIVE_TOKEN = 3
    scheduler = win32com.client.Dispatch('Schedule.Service')
    scheduler.Connect()
    root_folder = scheduler.GetFolder('\\')
    task_def = scheduler.NewTask(0)
    trigger = task_def.Triggers.Create(TASK_TRIGGER_LOGON)
    trigger.UserId = os.environ.get('USERNAME')
    action = task_def.Actions.Create(TASK_ACTION_EXEC)
    action.Path = os.path.join(os.getcwd(), 'venv\\Scripts\\pythonw.exe')
    action.Arguments = os.path.join(os.getcwd(), 'charging.py')
    action.WorkingDirectory = os.getcwd()
    task_def.RegistrationInfo.Description = ('Task for charging control'
                                             + ' of Tapo socket')
    task_def.Settings.Enabled = True
    task_def.Settings.StopIfGoingOnBatteries = False
    task_def.Settings.DisallowStartIfOnBatteries = False
    task_def.Settings.AllowHardTerminate = True
    task_def.Settings.StartWhenAvailable = True
    task_def.Settings.RunOnlyIfNetworkAvailable = False
    task_def.Settings.Enabled = True
    task_def.Settings.Hidden = True
    task_def.Settings.RunOnlyIfIdle = False
    task_def.Settings.UseUnifiedSchedulingEngine = True
    task_def.Settings.Priority = 7
    task_def.Settings.ExecutionTimeLimit = 'PT0S'
    root_folder.RegisterTaskDefinition(
        'Tapo Charging',
        task_def,
        TASK_CREATE_OR_UPDATE,
        '',
        '',
        TASK_LOGON_INTERACTIVE_TOKEN)
    task = root_folder.GetTask('Tapo Charging')
    task.Run(None)
    print('Task added to taskschd and running.')


def remove_from_taskschd():
    print('Removing from taskschd...')
    scheduler = win32com.client.Dispatch('Schedule.Service')
    scheduler.Connect()
    root_folder = scheduler.GetFolder('\\')
    task = root_folder.GetTask('Tapo Charging')
    task.Stop(0)
    root_folder.DeleteTask('Tapo Charging', 0)
    print('Task stopped and removed from taskschd.')
