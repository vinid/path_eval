import numpy as np
from sklearn.metrics import auc, roc_curve, f1_score, recall_score, precision_score, matthews_corrcoef, accuracy_score


def retrieval_metrics(y_target, y_predictions):
    p_5 = 0
    p_10 = 0

    for t, predictions in zip(y_target, y_predictions):
        if t in predictions[0:5]:
            p_5 += 1
        if t in predictions[0:10]:
            p_10 += 1

    return {"p@5": p_5/len(y_target), "p@10": p_10/len(y_target)}



def eval_metrics(y_true, y_pred, y_pred_proba = None, average_method='macro'):
    assert len(y_true) == len(y_pred)
    if y_pred_proba is None:
        auroc = np.nan
    else:
        fpr, tpr, thresholds = roc_curve(y_true, y_pred_proba)
        auroc = auc(fpr, tpr)
    f1 = f1_score(y_true, y_pred, average = average_method)
    precision = precision_score(y_true, y_pred, average = average_method)
    recall = recall_score(y_true, y_pred, average = average_method)
    mcc = matthews_corrcoef(y_true, y_pred)
    acc = accuracy_score(y_true, y_pred)
    tp,fp,tn,fn = 0,0,0,0
    for i in range(len(y_pred)):
        if y_true[i]==y_pred[i]==1:
           tp += 1
        if y_pred[i]==1 and y_true[i]!=y_pred[i]:
           fp += 1
        if y_true[i]==y_pred[i]==0:
           tn += 1
        if y_pred[i]==0 and y_true[i]!=y_pred[i]:
           fn += 1
    if (tp+fn) == 0: sensitivity = np.nan
    else: sensitivity = tp/(tp+fn) # recall
    if (tn+fp) == 0: specificity = np.nan
    else: specificity = tn/(tn+fp)
    if (tp+fp) == 0: ppv = np.nan
    else: ppv = tp/(tp+fp) # precision or positive predictive value (PPV)
    if (tn+fn) == 0: npv = np.nan
    else: npv = tn/(tn+fn) # negative predictive value (NPV)
    if (tp+tn+fp+fn) == 0: hitrate = np.nan
    else: hitrate = (tp+tn)/(tp+tn+fp+fn) # accuracy (ACC)
    performance = {'Accuracy': acc,
                   'AUC': auroc,
                   'F1': f1,
                   'precision': precision,
                   'recall': recall,
                   'mcc': mcc,
                   'tp': tp,
                   'fp': fp,
                   'tn': tn,
                   'fn': fn,
                   'sensitivity': sensitivity,
                   'specificity': specificity,
                   'ppv': ppv,
                   'npv': npv,
                   'hitrate': hitrate,
                   'instances' : len(y_true)}
    return performance