;;; 私有的符号 BEGIN
(defclass org-fledgling--plan ()
  ((trigger-time
    :documentation "任务被触发的时刻。"
    :initarg :trigger-time)))

(defclass org-fledgling--task ()
  ((brief
    :documentation "任务的简述"
    :initarg :brief)
   (plans
    :documentation "该任务设定的计划。"
    :initarg :plans)))

(defun org-fledgling--cons-task-plan ()
  "从当前光标所在的条目中构造出创建任务、计划所需要的数据。"
  (let* ((brief (nth 4 (org-heading-components)))
         (scheduled (org-entry-get nil "SCHEDULED"))
         ;; TODO: 此处还需要先将 SCHEDULED 转换为 TRIGGER-TIME 的格式才行。
         (plans nil))
    (when scheduled
      (setf plans (make-instance 'org-fledgling--plan
                                 :trigger-time scheduled)))
    (make-instance 'org-fledgling--task
                   :brief brief
                   :plans plans)))

(defun org-fledgling--make-command (program args)
  "生成以参数 ARGS 调用程序 PROGRAM 的命令。"
  (assert (stringp program))
  (dolist (arg args)
    (assert (or (numberp arg) (stringp arg))))

  (with-output-to-string
    (princ program)
    (dolist (arg args)
      (princ " ")
      (princ arg))))

(defun org-fledgling--run-fledgling (program args)
  "调用程序 fledgling，执行 ARGS 所指定的子命令。"
  (assert (stringp program))
  (dolist (arg args)
    (assert (or (numberp arg) (stringp arg))))

  (let ((command (org-fledgling--make-command program args)))
    (shell-command-to-string command)))
;;; 私有的符号 END

;;; 暴露的符号 BEGIN
(defvar *org-fledgling-program* nil
  "程序 fledgling 的可执行文件的路径。")
;;; 暴露的符号 END
