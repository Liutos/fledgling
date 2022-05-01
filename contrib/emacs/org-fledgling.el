;;; 私有的符号 BEGIN
(defclass org-fledgling--plan ()
  ((id
    :accessor org-fledgling--plan-id
    :documentation "计划的 ID。"
    :initarg :id)
   (trigger-time
    :accessor org-fledgling--plan-trigger-time
    :documentation "任务被触发的时刻。"
    :initarg :trigger-time
    :type string)))

(defclass org-fledgling--task ()
  ((brief
    :accessor org-fledgling--task-brief
    :documentation "任务的简述"
    :initarg :brief)
   (id
    :accessor org-fledgling--task-id
    :documentation "任务的 ID。"
    :initarg :id)
   (plans
    :documentation "该任务设定的计划。"
    :initarg :plans
    :reader org-fledgling--task-plans)))

(defvar *org-fledgling--property-plan-id* "PLAN_ID"
  "用于在 org-mode 的条目中存储对应的 fledgling 中的任务的计划的 ID 的属性名。")

(defvar *org-fledgling--property-task-id* "TASK_ID"
  "用于在 org-mode 的条目中存储对应的 fledgling 中的任务的 ID 的属性名。")

(defun org-fledgling--cons-task-plan ()
  "从当前光标所在的条目中构造出创建任务、计划所需要的数据。"
  (let* ((brief (nth 4 (org-heading-components)))
         (plan-id (org-entry-get nil *org-fledgling--property-plan-id*))
         (scheduled (org-entry-get nil "SCHEDULED"))
         (task-id (org-entry-get nil *org-fledgling--property-task-id*))
         (plans nil))
    (when scheduled
      (let* ((trigger-time (org-fledgling--scheduled-to-trigger-time scheduled))
             (plan (make-instance 'org-fledgling--plan
                                  :trigger-time trigger-time)))
        (when plan-id
          (setf (org-fledgling--plan-id plan) plan-id))

        (setf plans (list plan))))

    (when task-id
      (setf task-id (string-to-number task-id)))

    (make-instance 'org-fledgling--task
                   :brief brief
                   :id task-id
                   :plans plans)))

(defun org-fledgling--make-command (program args)
  "生成以参数 ARGS 调用程序 PROGRAM 的命令。"
  (assert (stringp program))
  (dolist (arg args)
    (assert (or (numberp arg) (stringp arg))))

  (with-output-to-string
    (princ program)
    (princ " --json")                   ; 要求 fledgling 以 JSON 格式将结果打印到标准输出，以便于解析。
    (dolist (arg args)
      (princ " ")
      (cond ((not (stringp arg))
             (princ arg))
            ((string-prefix-p "-" arg)
             ;; 命令行选项不需要引号。
             (princ arg))
            (t
             ;; 其余参数需要保留引号。
             (prin1 arg))))))

(defun org-fledgling--parse-plan-id (raw-output)
  "解析创建计划的命令所打印出的计划的 ID，以数值类型返回。"
  (message raw-output)
  (let ((parsed (json-parse-string raw-output)))
    (gethash "id" parsed)))

(defun org-fledgling--parse-task-id (raw-output)
  "解析创建任务的命令所打印出的任务的 ID，以数值类型返回。

参数 RAW-OUTPUT 是不加处理的、fledgling 的子命令 create-task 所打印的内容。"
  ;; json-parse-string 的文档见[这里](https://www.gnu.org/software/emacs/manual/html_node/elisp/Parsing-JSON.html#index-json_002dparse_002dstring)。
  (let ((parsed (json-parse-string raw-output)))
    (gethash "id" parsed)))

(defun org-fledgling--run-fledgling (program args)
  "调用程序 fledgling，执行 ARGS 所指定的子命令。"
  (assert (stringp program))
  (dolist (arg args)
    (assert (or (numberp arg) (stringp arg))))

  (let ((command (org-fledgling--make-command program args)))
    (message "即将执行的命令为：%s" command)
    (shell-command-to-string command)))

(defun org-fledgling--scheduled-to-trigger-time (scheduled)
  "将条目的 SCHEDULED 属性转换为 fledgling 的子命令 create-plan 的 --trigger-time 选项的格式。"
  (assert (stringp scheduled))
  ;; 为了能够支持形如<2019-06-15 Sat 14:25-14:55>这样的时间戳，会先用正则表达式提取date-to-time能够处理的部分
  (let* ((date (progn
                 (string-match "\\([0-9]+-[0-9]+-[0-9]+ .+ [0-9]+:[0-9]+\\)" scheduled)
                 (match-string 0 scheduled)))
         (lst (date-to-time date))
         (timestamp (+ (* (car lst) (expt 2 16))
                       (cadr lst))))
    (format-time-string "%Y-%m-%d %H:%M:%S" timestamp)))

(defun org-fledgling--sync-plan (plan task-id)
  "更新或创建一个计划。

其中，TASK-ID 是计划 PLAN 所属的任务的 ID。"
  (assert (typep plan org-fledgling--plan))
  (assert (integerp task-id))
  (let ((plan-id (org-fledgling--plan-id plan)))
    (cond ((null plan-id)
           (let* ((trigger-time (org-fledgling--plan-trigger-time plan))
                  (args (list "create-plan" "--task-id" task-id
                              "--trigger-time" trigger-time))
                  (raw-output (org-fledgling--run-fledgling *org-fledgling-program* args))
                  (plan-id (org-fledgling--parse-plan-id raw-output)))
             (message "创建了计划 %d" plan-id)
             (org-set-property *org-fledgling--property-plan-id* (number-to-string plan-id))))
          (t
           (let* ((trigger-time (org-fledgling--plan-trigger-time plan))
                  (args (list "change-plan" "--plan-id"plan-id 
                              "--trigger-time" trigger-time))
                  (raw-output (org-fledgling--run-fledgling *org-fledgling-program* args)))
             ;; 这里的 plan-id 来自于条目的属性，因此是个字符串类型。
             (message "修改了计划 %s" plan-id))))))

(defun org-fledgling--sync-task (task)
  "更新或创建一个任务"
  (assert (typep task org-fledgling--task))
  (cond ((null (org-fledgling--task-id task))
         (let* ((brief (org-fledgling--task-brief task))
                (args (list "create-task" "--brief" brief))
                (raw-output (org-fledgling--run-fledgling *org-fledgling-program* args))
                (task-id (org-fledgling--parse-task-id raw-output)))
           (message "新建了任务 %d" task-id)
           ;; 及早写入任务的 ID，以便出错重试时可以直接复用已创建的任务。
           (org-set-property *org-fledgling--property-task-id* (number-to-string task-id))
           task-id))
        (t
         (let* ((task-id (org-fledgling--task-id task))
                (brief (org-fledgling--task-brief task))
                (args (list "change-task" "--brief" brief "--task-id" task-id))
                (raw-output (org-fledgling--run-fledgling *org-fledgling-program* args)))
           (message "修改了任务 %d" task-id)
           task-id))))
;;; 私有的符号 END

;;; 暴露的符号 BEGIN
(defvar *org-fledgling-program* nil
  "程序 fledgling 的可执行文件的路径。")

(defun org-fledgling-sync-task-plan ()
  "为当前条目创建任务和计划。"
  (interactive)
  (let* ((task (org-fledgling--cons-task-plan))
         (plans (org-fledgling--task-plans task))
         (task-id (org-fledgling--sync-task task)))
    (when plans
      (org-fledgling--sync-plan (nth 0 (org-fledgling--task-plans task))
                                task-id))))
;;; 暴露的符号 END

(provide 'org-fledgling)
